"""Per-slice 3-stage chained vision prompting — process only NEW videos (v4).

v4 = the v3 all-videos loop, but with a cheap video-level pre-check against the
local slices/ folder: a video whose analysis JSON already exists (and covers
all its slices) is skipped WITHOUT any API calls. Only videos with no earlier
analysis are processed. A partially-analyzed video (interrupted run) is not
skipped — it is resumed, finishing just its missing slices.

Per processed video, per time slice (same chain as v2/v3):
  1. P1 -> R1  (vision, 1 frame):  road / locality / weather / lighting
  2. P2 (+R1 at {response}) -> R2  (vision, --frames2 frames): driving-style
     review + red/amber/green classification
  3. P3 (+R1 at {response1}, +R2 at {response2}) -> R3 (same dense frames):
     coaching suggestions for improving the driving

Output per video: slices/<video name>.slices.v2.json — same file and schema as
v2/v3, so all earlier results are recognized by the pre-check.

Usage:
    python videodb_slices_v4.py                    # all videos lacking analysis
    python videodb_slices_v4.py --only "Nagar"     # subset
    python videodb_slices_v4.py --limit 3          # max 3 slices per video (trial)
    python videodb_slices_v4.py --yes --cost       # no confirm prompt, cost meter
    python videodb_slices_v4.py --force            # reprocess even if analysis exists

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
SLICES_DIR = BASE_DIR / "slices"

PLACEHOLDER = "{response}"      # P2: where R1 goes
PLACEHOLDER1 = "{response1}"    # P3: where R1 goes
PLACEHOLDER2 = "{response2}"    # P3: where R2 goes

# Measured on the basic tier with frames1=1, frames2=5 (see session notes).
EST_CREDITS_PER_SLICE = 0.023

PROMPT1 = '''
Identify type of road (village road vs highway vs city road) , locality(rural/urban), weather condition (rain/summer) and lighting condition (day/night/lowlight)

'''
PROMPT2 = '''
Given the driving conditions: {response}\nReview the driving style for each video clip. We are looking for any of the following actions: tailgating, late breaking, harsh braking without visible clause, hitting speed breakers, Close passes on pedestrians, cyclists, and animals ; Slow or absent reaction to cut-ins; 	Running amber/red lights and rolling stops; Weaving and lane drift; 	Risky overtakes into oncoming traffic; Yo-yo following.\n Classify the driving style as red, amber or green. Red is for dangerous driving, amber is for risky driving, and green is for safe driving. Provide a brief explanation for your classification.
'''
PROMPT3 = '''
You are a driving coach reviewing this dashcam clip segment.

Driving conditions observed: {response1}

Driving-style review: {response2}

Based on the conditions, the review, and what is visible in the footage, give
the driver 2-3 specific, actionable suggestions to improve their driving in
this situation (e.g. following distance, speed for the conditions, positioning,
anticipation of hazards). Reference concrete things visible in the clip — avoid
generic advice. If the driving was safe, acknowledge what was done well and
suggest at most one refinement.
'''


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def fmt(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def read_prompt(args, which):
    """Prompt precedence: explicit --promptN > --promptN-file > built-in constant."""
    text = getattr(args, which)
    file = getattr(args, f"{which}_file")
    if text:
        return text
    if file:
        return Path(file).read_text(encoding="utf-8").strip()
    return {"prompt1": PROMPT1, "prompt2": PROMPT2, "prompt3": PROMPT3}[which].strip()


def build_p2(prompt2, r1):
    if PLACEHOLDER in prompt2:
        return prompt2.replace(PLACEHOLDER, r1)
    return f"{prompt2}\n\nPrevious analysis of this same clip:\n{r1}"


def build_p3(prompt3, r1, r2):
    out = prompt3
    if PLACEHOLDER1 in out:
        out = out.replace(PLACEHOLDER1, r1)
    else:
        out += f"\n\nDriving conditions observed:\n{r1}"
    if PLACEHOLDER2 in out:
        out = out.replace(PLACEHOLDER2, r2)
    else:
        out += f"\n\nDriving-style review:\n{r2}"
    return out


def get_scene_collection(video, slice_s, frames, SceneExtractionType):
    """Reuse an existing scene collection with matching config, else extract."""
    want = {"time": slice_s, "frame_count": frames}
    try:
        for entry in video.list_scene_collection():
            cid = entry.get("scene_collection_id")
            conf = entry.get("config") or {}
            if (int(conf.get("time", -1)) == slice_s
                    and int(conf.get("frame_count", -1)) == frames):
                sc = video.get_scene_collection(cid)
                if sc and sc.scenes:
                    return sc
    except Exception:
        pass
    print(f"    extracting {slice_s}s slices ({frames} frame(s) each)...")
    sc = video.extract_scenes(
        extraction_type=SceneExtractionType.time_based,
        extraction_config=want,
    )
    if not sc or not sc.scenes:
        raise RuntimeError("scene extraction returned no scenes")
    return sc


def out_path_for(video):
    return SLICES_DIR / f"{video.name}.slices.v2.json"


def load_existing(out_path):
    """start -> slice record for slices already fully processed (all 3 stages)."""
    if not out_path.exists():
        return {}
    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
        return {round(float(s["start"]), 1): s for s in data.get("slices", [])
                if s.get("response1") and s.get("response2") and s.get("response3")}
    except (json.JSONDecodeError, KeyError, ValueError):
        return {}


def expected_slices(video, slice_s, limit=None):
    n = -(-int(getattr(video, "length", 0) or 0) // slice_s)  # ceil
    if limit:
        n = min(n, limit)
    return max(n, 1)


def analysis_status(video, slice_s, limit=None):
    """('missing' | 'partial' | 'done', completed_slice_count) — from the
    slices/ folder only, no API calls."""
    out_path = out_path_for(video)
    if not out_path.exists():
        return "missing", 0
    n_done = len(load_existing(out_path))
    if n_done >= expected_slices(video, slice_s, limit):
        return "done", n_done
    return "partial", n_done


def save(out_path, payload):
    tmp = out_path.with_suffix(".part.json")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(out_path)


def process_video(video, args, conn, prompts, SceneExtractionType, InvalidRequestError):
    """Run the 3-stage chain over one video. Returns (processed, skipped, failed, credits)."""
    prompt1, prompt2, prompt3 = prompts

    sc = get_scene_collection(video, args.slice, args.frames1, SceneExtractionType)
    sc2 = (sc if args.frames2 == args.frames1 else
           get_scene_collection(video, args.slice, args.frames2, SceneExtractionType))
    dense_by_start = {round(float(s.start or 0), 1): s for s in sc2.scenes}

    scenes = sorted(sc.scenes, key=lambda s: s.start or 0)
    if args.limit:
        scenes = scenes[:args.limit]

    out_path = out_path_for(video)
    done = load_existing(out_path)

    payload = {
        "video": video.name,
        "video_id": video.id,
        "scene_collection_id": sc.id,
        "scene_collection_id_p2": sc2.id,
        "slice_seconds": args.slice,
        "frames_p1": args.frames1,
        "frames_p2": args.frames2,
        "model": args.model,
        "prompt1": prompt1,
        "prompt2": prompt2,
        "prompt3": prompt3,
        "generated": date.today().isoformat(),
        "slices": [],
    }

    prev_usage = conn.check_usage() if args.cost else None
    video_credits = 0.0
    processed = skipped = failed = 0
    total = len(scenes)
    for i, scene in enumerate(scenes, 1):
        key = round(float(scene.start or 0), 1)
        span = f"{fmt(scene.start)}-{fmt(scene.end)}"
        if key in done and not args.force:
            payload["slices"].append(done[key])
            skipped += 1
            continue
        rec = {"start": scene.start, "end": scene.end,
               "response1": None, "response2": None, "response3": None}
        scene_dense = dense_by_start.get(key, scene)
        try:
            r1 = scene.describe(prompt=prompt1, model_name=args.model)
            rec["response1"] = r1
            r2 = scene_dense.describe(prompt=build_p2(prompt2, r1 or ""),
                                      model_name=args.model)
            rec["response2"] = r2
            r3 = scene_dense.describe(prompt=build_p3(prompt3, r1 or "", r2 or ""),
                                      model_name=args.model)
            rec["response3"] = r3
            processed += 1
            note = ""
            if args.cost:
                cur = conn.check_usage()
                d = (cur.get("credit_used") or 0) - (prev_usage.get("credit_used") or 0)
                rec["credits"] = round(d, 5)
                video_credits += d
                prev_usage = cur
                note = f"  ({d:.4f} cr)"
            print(f"    [{i}/{total}] {span}  ok{note}")
        except InvalidRequestError as e:
            rec["error"] = str(e)[:300]
            failed += 1
            print(f"    [{i}/{total}] {span}  FAILED: {str(e)[:100]}")
        except Exception as e:
            rec["error"] = str(e)[:300]
            failed += 1
            print(f"    [{i}/{total}] {span}  ERROR: {str(e)[:100]}")
        payload["slices"].append(rec)
        save(out_path, payload)

    if processed or failed:
        save(out_path, payload)

    if args.index and any(s.get("response3") for s in payload["slices"]):
        indexable = []
        by_start = {round(float(s["start"]), 1): s for s in payload["slices"]
                    if s.get("response2") and s.get("response3")}
        for scene in sc2.scenes:
            rec = by_start.get(round(float(scene.start or 0), 1))
            if rec:
                scene.description = (f"{rec['response2']}\n\n"
                                     f"Suggestions: {rec['response3']}")
                indexable.append(scene)
        try:
            idx_id = video.index_scenes(scenes=indexable,
                                        name=f"sliced-v2 {video.name}"[:80])
            payload["scene_index_id"] = idx_id
            save(out_path, payload)
            print(f"    indexed online: {idx_id}")
        except InvalidRequestError as e:
            print(f"    online indexing failed: {str(e)[:150]}")

    return processed, skipped, failed, video_credits


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="only videos whose name contains this substring")
    ap.add_argument("--prompt1", help="P1; default: built-in PROMPT1")
    ap.add_argument("--prompt1-file")
    ap.add_argument("--prompt2", help="P2; {response} <- R1; default: built-in PROMPT2")
    ap.add_argument("--prompt2-file")
    ap.add_argument("--prompt3", help="P3; {response1}/{response2} <- R1/R2; "
                    "default: built-in PROMPT3 (driving coach)")
    ap.add_argument("--prompt3-file")
    ap.add_argument("--slice", type=int, default=20,
                    help="slice length in seconds (default 20)")
    ap.add_argument("--frames1", type=int, default=1,
                    help="frames per slice for P1 (default 1)")
    ap.add_argument("--frames2", type=int, default=5,
                    help="frames per slice for P2/P3 (default 5)")
    ap.add_argument("--model", choices=["basic", "pro", "ultra"], default="basic")
    ap.add_argument("--limit", type=int, help="max slices per video (trial runs)")
    ap.add_argument("--force", action="store_true",
                    help="reprocess videos/slices even if analysis exists")
    ap.add_argument("--index", action="store_true",
                    help="push R2+R3 per video as a searchable scene index")
    ap.add_argument("--cost", action="store_true",
                    help="measure credits per slice (adds one usage poll per slice)")
    ap.add_argument("--yes", action="store_true",
                    help="skip the cost-estimate confirmation prompt")
    args = ap.parse_args()

    load_env()
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")

    from videodb import connect, SceneExtractionType
    from videodb.exceptions import InvalidRequestError

    print("Connecting to VideoDB...")
    conn = connect(api_key=api_key)
    coll = conn.get_collection()
    videos = coll.get_videos()
    if args.only:
        needle = args.only.lower()
        videos = [v for v in videos if needle in (v.name or "").lower()]
    if not videos:
        sys.exit("No videos match." if args.only else "No videos in the collection.")
    videos.sort(key=lambda v: getattr(v, "length", 0) or 0)  # smallest first

    SLICES_DIR.mkdir(exist_ok=True)

    # THE v4 PRE-CHECK: consult the slices/ folder first. Videos whose analysis
    # is already complete are dropped here — zero API calls spent on them.
    todo, already = [], []
    for v in videos:
        status, n_done = analysis_status(v, args.slice, args.limit)
        if status == "done" and not args.force:
            already.append((v, n_done))
        else:
            todo.append((v, status, n_done))

    print(f"\n{len(videos)} video(s) checked against {SLICES_DIR.name}/: "
          f"{len(already)} already analyzed, {len(todo)} to process")
    for v, n in already:
        print(f"  = {v.name}  ({n} slices on disk)")
    if not todo:
        print("\nNothing to do — every video already has its analysis.")
        return
    print()
    total_pending = 0
    for v, status, n_done in todo:
        pending = expected_slices(v, args.slice, args.limit) - (0 if args.force else n_done)
        total_pending += max(pending, 0)
        tag = "resume" if status == "partial" else "new"
        print(f"  + {v.name}  [{tag}, ~{max(pending, 0)} slice(s)]")

    est = total_pending * EST_CREDITS_PER_SLICE
    balance = (conn.check_usage() or {}).get("credit_balance")
    print(f"\n~{total_pending} pending slice(s) -> estimated ~{est:.2f} credits "
          f"(balance: {balance:.2f})")
    if not args.yes:
        try:
            answer = input("Proceed? [y/N]: ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("Aborted — nothing spent. Use --only/--limit to narrow, --yes to skip this prompt.")
            return

    prompts = (read_prompt(args, "prompt1"), read_prompt(args, "prompt2"),
               read_prompt(args, "prompt3"))

    grand = {"processed": 0, "skipped": 0, "failed": 0, "credits": 0.0}
    for vi, (video, status, _) in enumerate(todo, 1):
        print(f"\n[{vi}/{len(todo)}] {video.name}  "
              f"({fmt(getattr(video, 'length', 0) or 0)}, {status})")
        try:
            p, s, f, c = process_video(video, args, conn, prompts,
                                       SceneExtractionType, InvalidRequestError)
        except Exception as e:
            print(f"    VIDEO FAILED: {str(e)[:150]}")
            grand["failed"] += 1
            continue
        grand["processed"] += p
        grand["skipped"] += s
        grand["failed"] += f
        grand["credits"] += c

    print(f"\n=== Run complete ===")
    print(f"videos already analyzed (untouched): {len(already)}")
    print(f"slices processed: {grand['processed']}, resumed-skipped: {grand['skipped']}, "
          f"failed: {grand['failed']}")
    if args.cost:
        final_balance = (conn.check_usage() or {}).get("credit_balance")
        print(f"credits spent: {grand['credits']:.4f}   balance now: {final_balance:.4f}")


if __name__ == "__main__":
    main()
