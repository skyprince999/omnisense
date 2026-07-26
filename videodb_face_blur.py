"""Upload a video to VideoDB and run a privacy face-blurring pipeline on it.

Pipeline stages (each is skipped if its output already exists — the run is resumable):

    upload  -> find the video in the collection by name, or upload it
    detect  -> video.understand(object_detection) to get per-frame `person` boxes.
               Optionally routed to a Sandbox Compute GPU running rtdetr-v2-r50vd
               instead of VideoDB's hosted detector.
    index   -> index the objects artifact for `query` + `aggregate`, then run a
               query/aggregate to show which scenes contain people. This is the
               "search or query" view of the same artifact.
    render  -> build an Editor Timeline that blurs the people and generate a stream.

Three ways to get the blur out, two of them on VideoDB:

  --mode segment  (default) Whole-frame Filter.blur for every time range that
                  contains a person. One track, no compositing. Coarse — on
                  people-heavy footage it blurs most of the video — but it is the
                  only VideoDB-native redaction that renders predictably.

  --mode region   EXPERIMENTAL / KNOWN BROKEN. Intended as real per-face pixel
                  blur: crop a second reference to the same video down to the face
                  box, blur it, position it back over the base. Measured against a
                  calibration render (2026-07-26) the Editor instead scales a
                  cropped overlay up to fill the whole canvas, and `fit`, `scale`,
                  `offset` and `position` had no effect on the result — so the
                  blur does not stay inside the face box. Kept only so the finding
                  is reproducible; do not ship its output.

  --local-render OUT.mp4
                  Exact per-face blur, done locally with ffmpeg + OpenCV using the
                  boxes VideoDB detected. This is the mode that actually produces a
                  correctly face-blurred video: VideoDB does the understanding, the
                  local GPU box does the pixels.

Face boxes: VideoDB's object detector is COCO, so it emits `person`, not `face`.
This script derives a head region from each person box (top --head-frac of the
box height, centre --head-width of its width, plus --pad). That is a heuristic,
not face detection; widen --head-frac/--pad if faces peek out of the blur.

Usage:
    python videodb_face_blur.py --dry-run              # plan only, no API calls that cost
    python videodb_face_blur.py                        # full run, hosted detector
    python videodb_face_blur.py --sandbox              # run detection on a Sandbox GPU
    python videodb_face_blur.py --stages render        # re-render from cached detections
    python videodb_face_blur.py --stages "" --local-render "faceblur/blurred.mp4"
                                                       # exact local face blur, no re-render
    python videodb_face_blur.py --file "path/to.mp4" --download

Requires VIDEODB_API_KEY in the environment or in .env next to this script.
Note: the installed SDK reads VIDEO_DB_API_KEY (underscore); load_env() sets both.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_VIDEO = BASE_DIR / "Calliberation Videos" / "stich" / "stitched_2x.mp4"
OUT_DIR = BASE_DIR / "faceblur"
MAX_UPLOAD_MB = 1000  # current-tier upload limit; split larger files first
ALL_STAGES = ("upload", "detect", "index", "render")


# ---------------------------------------------------------------- environment


def load_env():
    """Load .env next to this script and mirror the key under both spellings.

    The docs and this project's .env use VIDEODB_API_KEY; the installed SDK
    reads VIDEO_DB_API_KEY. Set whichever is missing from whichever is present.
    """
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    key = os.environ.get("VIDEODB_API_KEY") or os.environ.get("VIDEO_DB_API_KEY")
    if not key:
        sys.exit("No API key found. Set VIDEODB_API_KEY in the environment or .env.")
    os.environ["VIDEODB_API_KEY"] = key
    os.environ["VIDEO_DB_API_KEY"] = key


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


# ------------------------------------------------------------------ state I/O


def state_path(stem):
    return OUT_DIR / f"{stem}.state.json"


def load_state(stem):
    p = state_path(stem)
    return json.loads(p.read_text()) if p.exists() else {}


def save_state(stem, state):
    OUT_DIR.mkdir(exist_ok=True)
    state_path(stem).write_text(json.dumps(state, indent=2))


def write_json(path, data):
    OUT_DIR.mkdir(exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


# -------------------------------------------------------------- stage: upload


def find_or_upload(coll, path, name, force):
    """Return a Video for `path`, reusing an existing upload with the same name."""
    if not force:
        for v in coll.get_videos():
            if getattr(v, "name", None) == name:
                print(f"  reusing existing upload: {v.id}  ({v.name})")
                return v

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        sys.exit(f"{path.name} is {size_mb:.0f} MB, over the {MAX_UPLOAD_MB} MB "
                 f"upload limit. Split it first with split_video.py.")

    print(f"  uploading {path.name} ({size_mb:.0f} MB) ...")
    t0 = time.time()
    video = coll.upload(file_path=str(path), media_type="video", name=name)
    print(f"  uploaded in {time.time() - t0:.0f}s -> {video.id}")
    return video


# -------------------------------------------------------------- stage: detect


def start_sandbox(conn, tier):
    from videodb import SandboxTier

    tier_value = {"small": SandboxTier.small, "medium": SandboxTier.medium}[tier]
    print(f"  creating {tier} sandbox with rtdetr-v2-r50vd ...")
    sandbox = conn.create_sandbox(
        tier=tier_value,
        name="face-blur-detect",
        models=["rtdetr-v2-r50vd"],
    )
    print(f"  sandbox {sandbox.id} provisioning (billed per hour while running) ...")
    sandbox.wait_for_ready(timeout=600, interval=5)
    print(f"  sandbox ready: {sandbox.status}")
    return sandbox


def run_detection(conn, video, args, on_understanding=None):
    """Run the object_detection analyzer and return (objects_output, analyzer, id).

    `on_understanding` is called with the understanding id as soon as the run is
    submitted, so a crash later in this function cannot lose the handle to a run
    that has already been paid for.
    """
    sandbox = start_sandbox(conn, args.tier) if args.sandbox else None
    try:
        config = {}
        if sandbox:
            config = {"model": "rtdetr-v2-r50vd", "sandbox_id": sandbox.id}

        analyzers = [{
            "type": "object_detection",
            "name": "objects",
            "sampling": {"strategy": "interval", "every": args.every},
        }]
        if config:
            analyzers[0]["config"] = config

        print(f"  understanding: object_detection, {args.segment_seconds}s segments, "
              f"1 frame every {args.every}s"
              + (f", model=rtdetr-v2-r50vd on {sandbox.id}" if sandbox else ", hosted model"))
        understanding = video.understand(
            analyzers=analyzers,
            segmentation={"type": "time", "seconds": args.segment_seconds},
        )
        print(f"  understanding {understanding.id} running (this takes a while) ...")
        if on_understanding:
            on_understanding(understanding.id)
        understanding.wait_until_complete(timeout=args.timeout, poll_interval=15)

        analyzer = understanding.get_analyzer("objects", refresh=True)
        if not analyzer.is_successful:  # property, not a method
            sys.exit(f"object_detection analyzer finished as {analyzer.status}. "
                     f"Understanding id {understanding.id} — re-run with --force-detect, "
                     f"or drop --sandbox to use the hosted model.")
        return analyzer.get_output(), analyzer, understanding.id
    finally:
        if sandbox:
            print(f"  stopping sandbox {sandbox.id} (billing stops here) ...")
            try:
                sandbox.stop()
                sandbox.wait_for_stop(timeout=180, interval=5)
                print(f"  sandbox final status: {sandbox.status}")
            except Exception as e:  # never let cleanup mask a real error
                print(f"  WARNING: could not confirm sandbox stop: {e}\n"
                      f"  Stop it manually: conn.get_sandbox('{sandbox.id}').stop()")


# -------------------------------------------------- detections -> face boxes


def iter_person_frames(objects, min_score):
    """Yield (timestamp, [person box, ...]) for each sampled frame, in time order.

    Boxes are normalized xyxy, matching the rest of this project's convention.
    """
    frames = []
    for scene in objects.get("scenes", []):
        scene_start = float(scene.get("start", 0.0))
        for frame in scene.get("data", {}).get("frames", []):
            # The live artifact names this `timestamp_sec` and it is absolute, but
            # the published docs show `timestamp`. Accept either; refuse to guess if
            # neither is present, because defaulting to 0 would silently pile every
            # face in a scene onto the scene's first instant.
            raw = frame.get("timestamp_sec", frame.get("timestamp"))
            if raw is None:
                raise ValueError(
                    f"frame {frame.get('frame_id')} has no timestamp_sec/timestamp field; "
                    f"the analyzer output shape changed — inspect the objects json"
                )
            ts = float(raw)
            if ts < scene_start:  # tolerate a scene-relative variant
                ts += scene_start
            boxes = []
            for det in frame.get("detections", []):
                if det.get("label") != "person":
                    continue
                if float(det.get("score", 0.0)) < min_score:
                    continue
                box = det.get("box", {})
                coords = box.get("box") if isinstance(box, dict) else box
                if not coords or len(coords) != 4:
                    continue
                boxes.append([float(c) for c in coords])
            frames.append((ts, boxes))
    frames.sort(key=lambda f: f[0])
    return frames


def head_region(person_box, head_frac, head_width, pad):
    """Approximate the head/face region inside a normalized person box."""
    x1, y1, x2, y2 = person_box
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    w, h = x2 - x1, y2 - y1
    if w <= 0 or h <= 0:
        return None

    cx = x1 + w / 2
    hw = w * head_width / 2
    hx1, hx2 = cx - hw, cx + hw
    hy1, hy2 = y1, y1 + h * head_frac

    hx1, hy1 = max(0.0, hx1 - pad), max(0.0, hy1 - pad)
    hx2, hy2 = min(1.0, hx2 + pad), min(1.0, hy2 + pad)
    if hx2 - hx1 <= 0.001 or hy2 - hy1 <= 0.001:
        return None
    return [hx1, hy1, hx2, hy2]


def box_center(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def box_area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def union(a, b):
    return [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]


def link_tracks(frames, args):
    """Group per-frame face boxes into short-lived tracks.

    One overlay clip per sampled face would mean thousands of clips, so faces are
    linked across consecutive sampled frames by centre proximity and each track
    becomes a single clip covering the union of its boxes. A track is closed when
    it runs longer than --max-track-s or when the union has grown far beyond the
    faces it contains (a moving face would otherwise smear a huge blur patch).
    """
    open_tracks = []   # {"box": union, "start": t, "end": t, "last": box, "n": int, "area": float}
    done = []

    for ts, person_boxes in frames:
        faces = [f for f in (head_region(b, args.head_frac, args.head_width, args.pad)
                             for b in person_boxes) if f]
        faces = [f for f in faces if box_area(f) >= args.min_area]

        still_open = []
        for tr in open_tracks:
            # find the nearest unclaimed face to this track's last box
            best, best_d = None, None
            lcx, lcy = box_center(tr["last"])
            for f in faces:
                fcx, fcy = box_center(f)
                d = ((fcx - lcx) ** 2 + (fcy - lcy) ** 2) ** 0.5
                if best_d is None or d < best_d:
                    best, best_d = f, d

            if best is None or best_d > args.link_dist:
                done.append(tr)
                continue

            faces.remove(best)
            new_union = union(tr["box"], best)
            mean_area = (tr["area"] + box_area(best)) / (tr["n"] + 1)
            too_smeared = box_area(new_union) > mean_area * args.max_smear
            too_long = (ts + args.every) - tr["start"] > args.max_track_s

            if too_smeared or too_long:
                done.append(tr)
                still_open.append({"box": best, "start": ts, "end": ts + args.every,
                                   "last": best, "n": 1, "area": box_area(best)})
            else:
                tr.update(box=new_union, end=ts + args.every, last=best,
                          n=tr["n"] + 1, area=tr["area"] + box_area(best))
                still_open.append(tr)

        for f in faces:  # unmatched faces start new tracks
            still_open.append({"box": f, "start": ts, "end": ts + args.every,
                               "last": f, "n": 1, "area": box_area(f)})
        open_tracks = still_open

    done.extend(open_tracks)
    done.sort(key=lambda t: (t["start"], t["box"][0]))
    return [{"start": round(t["start"], 3), "end": round(t["end"], 3),
             "box": [round(c, 4) for c in t["box"]], "frames": t["n"]} for t in done]


def merge_intervals(tracks, duration, min_len=0.0):
    """Collapse face tracks into merged [start, end] ranges (segment mode)."""
    spans = sorted(([t["start"], t["end"]] for t in tracks), key=lambda s: s[0])
    merged = []
    for s in spans:
        if merged and s[0] <= merged[-1][1] + 0.001:
            merged[-1][1] = max(merged[-1][1], s[1])
        else:
            merged.append(list(s))
    out = []
    for s, e in merged:
        s, e = max(0.0, s), min(duration, e)
        if e - s >= min_len:
            out.append([round(s, 3), round(e, 3)])
    return out


# -------------------------------------------------------------- stage: render


def build_region_timeline(conn, video, duration, tracks, args):
    """Base video on z=0, one cropped+blurred overlay per face track on z=1."""
    from videodb.editor import Clip, Crop, Fit, Filter, Offset, Position, Timeline, Track, VideoAsset

    if len(tracks) > args.max_overlays:
        # keep the largest boxes — they are the ones a viewer would actually recognise
        tracks = sorted(tracks, key=lambda t: box_area(t["box"]), reverse=True)[:args.max_overlays]
        tracks.sort(key=lambda t: t["start"])
        print(f"  capped overlays at --max-overlays={args.max_overlays} "
              f"(largest boxes kept)")

    timeline = Timeline(conn)

    base = Track(z_index=0)
    base.add_clip(0, Clip(asset=VideoAsset(id=video.id, start=0), duration=round(duration, 3)))
    timeline.add_track(base)

    overlay = Track(z_index=1)
    for t in tracks:
        x1, y1, x2, y2 = t["box"]
        start = max(0.0, t["start"])
        dur = round(min(t["end"], duration) - start, 3)
        if dur <= 0.04:
            continue

        # Crop everything except the face box out of a second reference to the
        # same video, so the clip *is* the face patch.
        if args.crop_units == "pixels":
            w, h = args.canvas_width, args.canvas_height
            crop = Crop(left=int(x1 * w), right=int((1 - x2) * w),
                        top=int(y1 * h), bottom=int((1 - y2) * h))
        else:
            crop = Crop(left=round(x1, 4), right=round(1 - x2, 4),
                        top=round(y1, 4), bottom=round(1 - y2, 4))

        cx, cy = box_center(t["box"])
        overlay.add_clip(round(start, 3), Clip(
            asset=VideoAsset(id=video.id, start=round(start, 3), volume=0, crop=crop),
            duration=dur,
            filter=Filter.blur,
            fit=Fit.none,          # keep the patch at native size; do not refill the canvas
            position=Position.center,
            offset=Offset(x=round(cx - 0.5, 4), y=round(0.5 - cy, 4)),  # +y is up
            z_index=1,
        ))
    timeline.add_track(overlay)
    print(f"  timeline: 1 base clip + {len(overlay.clips)} blurred face overlays")
    return timeline


def build_segment_timeline(conn, video, duration, intervals, args):
    """One track; every range containing a person plays through Filter.blur."""
    from videodb.editor import Clip, Filter, Timeline, Track, VideoAsset

    timeline = Timeline(conn)
    track = Track(z_index=0)

    cursor, blurred, clean = 0.0, 0, 0
    for s, e in intervals:
        if s - cursor > 0.04:
            track.add_clip(round(cursor, 3), Clip(
                asset=VideoAsset(id=video.id, start=round(cursor, 3)),
                duration=round(s - cursor, 3)))
            clean += 1
        track.add_clip(round(s, 3), Clip(
            asset=VideoAsset(id=video.id, start=round(s, 3)),
            duration=round(e - s, 3), filter=Filter.blur))
        blurred += 1
        cursor = e

    if duration - cursor > 0.04:
        track.add_clip(round(cursor, 3), Clip(
            asset=VideoAsset(id=video.id, start=round(cursor, 3)),
            duration=round(duration - cursor, 3)))
        clean += 1

    timeline.add_track(track)
    covered = sum(e - s for s, e in intervals)
    print(f"  timeline: {blurred} blurred + {clean} clean clips "
          f"({covered:.1f}s of {duration:.1f}s blurred, {covered / duration * 100:.0f}%)")
    return timeline


# --------------------------------------------------------- stage: index/query


def index_and_query(video, analyzer, args):
    """Index the objects artifact, then query/aggregate it for people."""
    try:
        # Field names are the artifact's own dotted paths. The object_detection
        # artifact puts its per-scene rollup under `summary`, so the indexable
        # names are summary.labels / summary.counts — not the `object_labels`
        # spelling in the docs, which the API rejects outright.
        video.index(
            source=analyzer,
            name="objects",
            use_for=["query", "aggregate"],
            fields={"filter": ["summary.labels", "summary.counts"],
                    "aggregate": ["summary.labels"]},
        )
        print("  indexed objects artifact for query + aggregate")
    except Exception as e:
        print(f"  index step failed ({e}); continuing with the raw artifact")
        return None

    try:
        results = video.query(
            index_name="objects",
            filter={"summary.labels": {"contains": "person"}},
            limit=args.query_limit,
        )
        shots = list(getattr(results, "shots", None) or [])
        print(f"  query 'summary.labels contains person' -> {len(shots)} scenes")
        for shot in shots[:5]:
            print(f"    {getattr(shot, 'start', '?')}s - {getattr(shot, 'end', '?')}s")
        if len(shots) > 5:
            print(f"    ... and {len(shots) - 5} more")
    except Exception as e:
        print(f"  query failed: {e}")

    try:
        agg = video.aggregate(index_name="objects", group_by="summary.labels", metric="count")
        rows = agg.get("results", agg) if isinstance(agg, dict) else agg
        print(f"  aggregate by object_labels: {json.dumps(rows)[:400]}")
    except Exception as e:
        print(f"  aggregate failed: {e}")


# -------------------------------------------------------------------- driver


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", type=Path, default=DEFAULT_VIDEO,
                   help="video to upload and blur (default: the stitched 2x calibration video)")
    p.add_argument("--name", help="upload name (default: filename without extension)")
    p.add_argument("--mode", choices=["region", "segment"], default="region",
                   help="region = per-face pixel blur (default); segment = whole-frame blur")
    p.add_argument("--stages", default=",".join(ALL_STAGES),
                   help=f"comma-separated subset of {','.join(ALL_STAGES)}")
    p.add_argument("--dry-run", action="store_true",
                   help="plan the run and show cached detection stats; no uploads or renders")

    g = p.add_argument_group("detection")
    g.add_argument("--sandbox", action="store_true",
                   help="run detection on a Sandbox Compute GPU (rtdetr-v2-r50vd, billed hourly)")
    g.add_argument("--tier", choices=["small", "medium"], default="small",
                   help="sandbox tier (small = $1/hr, enough for rtdetr)")
    g.add_argument("--every", type=float, default=1.0,
                   help="seconds between sampled frames (default 1.0)")
    g.add_argument("--segment-seconds", type=float, default=10.0,
                   help="fixed-length scene segmentation in seconds (default 10)")
    g.add_argument("--timeout", type=int, default=5400,
                   help="seconds to wait for the understanding run (default 5400)")
    g.add_argument("--force-upload", action="store_true", help="upload even if the name exists")
    g.add_argument("--force-detect", action="store_true", help="re-run detection, ignore cache")

    g = p.add_argument_group("face region heuristic")
    g.add_argument("--min-score", type=float, default=0.35, help="min person confidence")
    g.add_argument("--head-frac", type=float, default=0.32,
                   help="fraction of the person box height treated as head (default 0.32)")
    g.add_argument("--head-width", type=float, default=0.75,
                   help="fraction of the person box width treated as head (default 0.75)")
    g.add_argument("--pad", type=float, default=0.02,
                   help="extra normalized padding around the head box (default 0.02)")
    g.add_argument("--min-area", type=float, default=0.00015,
                   help="drop face boxes smaller than this normalized area")

    g = p.add_argument_group("region-mode overlays")
    g.add_argument("--max-track-s", type=float, default=2.0,
                   help="max seconds one overlay clip may span (default 2)")
    g.add_argument("--link-dist", type=float, default=0.10,
                   help="max normalized centre distance to link a face across frames")
    g.add_argument("--max-smear", type=float, default=4.0,
                   help="close a track when its union box exceeds this x its mean box area")
    g.add_argument("--max-overlays", type=int, default=400,
                   help="cap on overlay clips; largest boxes win (default 400)")
    g.add_argument("--crop-units", choices=["relative", "pixels"], default="relative",
                   help="Crop() units. Docs say relative 0..1; the SDK docstring says "
                        "pixels. Flip this if the blur patches land wrong.")
    g.add_argument("--canvas-width", type=int, default=1920)
    g.add_argument("--canvas-height", type=int, default=1080)

    g = p.add_argument_group("output")
    g.add_argument("--query-limit", type=int, default=100)
    g.add_argument("--download", action="store_true",
                   help="also request a downloadable mp4 of the blurred render")
    return p.parse_args()


def main():
    args = parse_args()
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    for s in stages:
        if s not in ALL_STAGES:
            sys.exit(f"unknown stage {s!r}; choose from {', '.join(ALL_STAGES)}")

    path = args.file
    if not path.exists():
        sys.exit(f"not found: {path}")
    stem = path.stem
    name = args.name or stem
    OUT_DIR.mkdir(exist_ok=True)

    objects_file = OUT_DIR / f"{stem}.objects.json"
    faces_file = OUT_DIR / f"{stem}.faces.json"
    state = load_state(stem)

    duration = ffprobe_duration(path)
    print(f"video : {path.name}")
    print(f"length: {duration:.1f}s" if duration else "length: unknown")
    print(f"mode  : {args.mode}   stages: {', '.join(stages)}   "
          f"detector: {'sandbox rtdetr-v2-r50vd' if args.sandbox else 'hosted default'}")
    print(f"out   : {OUT_DIR}")

    if args.dry_run:
        print("\n[dry run]")
        print(f"  would upload as   : {name}")
        print(f"  cached detections : {'yes' if objects_file.exists() else 'no'} ({objects_file})")
        print(f"  known video id    : {state.get('video_id', '-')}")
        if objects_file.exists():
            objects = json.loads(objects_file.read_text())
            frames = iter_person_frames(objects, args.min_score)
            with_people = sum(1 for _, b in frames if b)
            tracks = link_tracks(frames, args)
            print(f"  sampled frames    : {len(frames)} ({with_people} contain a person)")
            print(f"  face tracks       : {len(tracks)}")
            if duration:
                iv = merge_intervals(tracks, duration)
                covered = sum(e - s for s, e in iv)
                print(f"  segment-mode blur : {len(iv)} ranges, {covered:.1f}s "
                      f"({covered / duration * 100:.0f}% of the video)")
        return

    load_env()
    import videodb

    conn = videodb.connect()
    coll = conn.get_collection()

    # ---- upload ----------------------------------------------------------
    video = None
    if "upload" in stages:
        print("\n[upload]")
        video = find_or_upload(coll, path, name, args.force_upload)
        state["video_id"] = video.id
        state["name"] = name
        save_state(stem, state)
    elif state.get("video_id"):
        video = coll.get_video(state["video_id"])
        print(f"\n[upload] skipped, using cached video id {video.id}")
    else:
        sys.exit("no cached video id; run with the upload stage included")

    # The Editor validates clip durations against VideoDB's own stored length, which
    # can sit slightly below ffprobe's (235.0 vs 235.233 on the calibration video).
    # Take the smaller of the two, or a clip that covers the whole video is rejected.
    server_length = float(getattr(video, "length", 0.0) or 0.0)
    if server_length:
        if duration and server_length < duration:
            print(f"  clamping duration {duration:.3f}s -> {server_length:.3f}s "
                  f"(VideoDB's stored length)")
        duration = min(duration, server_length) if duration else server_length
    if not duration:
        sys.exit("could not determine video duration (ffprobe failed and "
                 "VideoDB reported no length)")

    # ---- detect ----------------------------------------------------------
    objects, analyzer = None, None
    if "detect" in stages and (args.force_detect or not objects_file.exists()):
        print("\n[detect]")

        def remember(uid):
            state["understanding_id"] = uid
            save_state(stem, state)

        objects, analyzer, understanding_id = run_detection(conn, video, args, remember)
        write_json(objects_file, objects)
        state["understanding_id"] = understanding_id
        save_state(stem, state)
        print(f"  saved detections -> {objects_file}")
    elif objects_file.exists():
        objects = json.loads(objects_file.read_text())
        print(f"\n[detect] skipped, using cached {objects_file.name}")
    else:
        sys.exit("no detections available; include the detect stage")

    frames = iter_person_frames(objects, args.min_score)
    with_people = sum(1 for _, b in frames if b)
    total_people = sum(len(b) for _, b in frames)
    print(f"  {len(frames)} sampled frames, {with_people} with a person, "
          f"{total_people} person boxes above score {args.min_score}")

    tracks = link_tracks(frames, args)
    intervals = merge_intervals(tracks, duration)
    write_json(faces_file, {
        "video_id": video.id,
        "source": path.name,
        "duration": duration,
        "box_format": "normalized xyxy",
        "derived_from": "person detections, head heuristic",
        "params": {"min_score": args.min_score, "head_frac": args.head_frac,
                   "head_width": args.head_width, "pad": args.pad},
        "face_tracks": tracks,
        "blur_intervals": intervals,
    })
    print(f"  {len(tracks)} face tracks over {len(intervals)} time ranges "
          f"-> {faces_file.name}")

    if not tracks:
        print("\nNo people detected above the threshold — nothing to blur. "
              "Try a lower --min-score or a denser --every.")
        return

    # ---- index + query ---------------------------------------------------
    if "index" in stages:
        print("\n[index + query]")
        if analyzer is None:
            uid = state.get("understanding_id")
            if uid:
                try:
                    analyzer = video.get_understanding(uid).get_analyzer("objects")
                except Exception as e:
                    print(f"  could not reload analyzer {uid}: {e}")
        if analyzer is None:
            print("  no analyzer handle in this run (detections came from cache); "
                  "re-run with --force-detect to index a fresh artifact")
        else:
            index_and_query(video, analyzer, args)

    # ---- render ----------------------------------------------------------
    if "render" in stages:
        print("\n[render]")
        if args.mode == "region":
            timeline = build_region_timeline(conn, video, duration, tracks, args)
        else:
            timeline = build_segment_timeline(conn, video, duration, intervals, args)

        stream_url = timeline.generate_stream()
        state["stream_url"] = stream_url
        state["player_url"] = getattr(timeline, "player_url", None)
        state["mode"] = args.mode
        save_state(stem, state)

        print(f"\n  stream : {stream_url}")
        if getattr(timeline, "player_url", None):
            print(f"  player : {timeline.player_url}")

        if args.download:
            try:
                info = timeline.download_stream(stream_url)
                state["download"] = info
                save_state(stem, state)
                print(f"  download: {json.dumps(info)[:400]}")
            except Exception as e:
                print(f"  download request failed: {e}")

        print(f"\n  state saved -> {state_path(stem)}")


if __name__ == "__main__":
    main()
