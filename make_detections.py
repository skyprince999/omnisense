"""Run a single-pass YOLO26 detection over the stitched dashcam clips.

For each top-level stitched/<clip>.mp4 this decodes the video with ffmpeg
(robust to the corrupt/dropped frames common in dashcam footage), runs one
forward pass of YOLO26 per frame, keeps only person + road-vehicle boxes, and
writes the results as detections/<clip>.detections.json — a compact,
resolution-independent record the frontend overlays on playback in sync with
video.currentTime. Coordinates are normalized (0..1) so they map onto the
player at any display size.

Optionally (--render) it also writes an annotated preview mp4 to detections/
so you can eyeball the detections without the frontend.

Usage:
    python make_detections.py "stitched/<clip>.mp4"     # one video
    python make_detections.py --all                     # every top-level stitched/*.mp4,
                                                        # smallest first, skipping done ones
    python make_detections.py --all --force             # re-run even if JSON exists
    python make_detections.py --all --render            # also write annotated preview mp4s
    python make_detections.py <clip>.mp4 --model yolo26s.pt   # larger model, slower/better

Requires: ultralytics (torch/CUDA), opencv-python, and ffmpeg/ffprobe on PATH.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).parent
STITCHED_DIR = BASE_DIR / "stitched"
DETECT_DIR = BASE_DIR / "detections"

# COCO class ids we care about: person + the road vehicles + the animals a
# dashcam realistically sees on Indian roads. (train=6 and the zoo animals —
# elephant/bear/zebra/giraffe — and bird are intentionally omitted.)
PERSON_IDS = {0}
VEHICLE_IDS = {1, 2, 3, 5, 7}
ANIMAL_IDS = {15, 16, 17, 18, 19}  # cat, dog, horse, sheep, cow

KEEP_CLASSES = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
    15: "cat",
    16: "dog",
    17: "horse",
    18: "sheep",
    19: "cow",
}

# Draw colors (BGR) for the optional annotated preview.
PERSON_COLOR = (0, 200, 255)   # amber-ish for people
VEHICLE_COLOR = (80, 220, 80)  # green for vehicles
ANIMAL_COLOR = (255, 150, 60)  # blue-ish for animals


def color_for(cls):
    if cls in PERSON_IDS:
        return PERSON_COLOR
    if cls in ANIMAL_IDS:
        return ANIMAL_COLOR
    return VEHICLE_COLOR

# A JSON output counts as "done" only if it covers at least this fraction of the
# source's frames — guards against truncated runs from an earlier crash.
COMPLETE_FRAC = 0.98


def load_model(name, device):
    from ultralytics import YOLO

    print(f"Loading {name} ...", flush=True)
    model = YOLO(name)
    model.to(device)
    return model


def probe_video(path):
    """Return (width, height, fps, nb_frames) via ffprobe."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,avg_frame_rate,nb_frames",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    s = json.loads(out)["streams"][0]
    num, den = s["avg_frame_rate"].split("/")
    fps = float(num) / float(den) if float(den) else 30.0
    nb = int(s.get("nb_frames") or 0)
    return int(s["width"]), int(s["height"]), fps, nb


def start_ffmpeg_reader(src, w, h):
    """Decode src to a stream of raw rgb24 frames of size w x h. Corrupt frames
    are skipped by the decoder instead of ending the stream early."""
    cmd = [
        "ffmpeg", "-loglevel", "error",
        "-i", str(src),
        "-vf", f"scale={w}:{h}",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)


def start_ffmpeg_writer(out_path, width, height, fps):
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{width}x{height}", "-r", f"{fps}",
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
        "-movflags", "+faststart",
        str(out_path),
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def output_is_complete(src, out_json):
    """True if the JSON exists and covers ~as many frames as src."""
    if not out_json.exists():
        return False
    try:
        data = json.loads(out_json.read_text(encoding="utf-8"))
        _, _, _, src_n = probe_video(src)
    except Exception:
        return False
    covered = int(data.get("frames_processed", 0))
    if src_n == 0:
        return covered > 0
    return covered >= COMPLETE_FRAC * src_n


def draw_boxes(frame_bgr, dets, w, h):
    """Draw normalized dets [cls, conf, x1, y1, x2, y2] onto a BGR frame."""
    for cls, conf, x1, y1, x2, y2 in dets:
        color = color_for(cls)
        p1 = (int(x1 * w), int(y1 * h))
        p2 = (int(x2 * w), int(y2 * h))
        cv2.rectangle(frame_bgr, p1, p2, color, 2)
        label = f"{KEEP_CLASSES[cls]} {conf:.2f}"
        cv2.putText(frame_bgr, label, (p1[0], max(p1[1] - 5, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    return frame_bgr


def process_video(src, model, args):
    src_w, src_h, fps, nb_frames = probe_video(src)

    # Decode at a fixed inference width; store normalized coords so the boxes
    # map back onto the player at the source (or any) resolution.
    infer_w = min(args.width, src_w)
    infer_h = int(round(src_h * infer_w / src_w / 2) * 2)  # even for the writer
    frame_bytes = infer_w * infer_h * 3

    out_json = DETECT_DIR / f"{src.stem}.detections.json"
    tmp_json = DETECT_DIR / f"{src.stem}.detections.part.json"

    keep_ids = sorted(KEEP_CLASSES)

    print(f"Source: {src.name}  {src_w}x{src_h} @ {fps:.2f} fps, {nb_frames} frames", flush=True)
    reader = start_ffmpeg_reader(src, infer_w, infer_h)

    writer = None
    if args.render:
        out_mp4 = DETECT_DIR / f"{src.stem}.detect.mp4"
        writer = start_ffmpeg_writer(out_mp4, infer_w, infer_h, fps)

    frames = []          # per-frame list of detections (index == frame number)
    frame_idx = 0        # source frames seen
    processed = 0        # frames actually inferred (respects --stride)
    total_dets = 0
    batch = []           # list of (frame_index, rgb_frame)

    def flush(batch):
        nonlocal total_dets
        rgb = [f for _, f in batch]
        # verbose=False keeps ultralytics from printing a line per frame.
        results = model.predict(
            rgb, imgsz=args.imgsz, conf=args.conf, classes=keep_ids,
            device=args.device, verbose=False,
        )
        for (fi, rgb_frame), res in zip(batch, results):
            dets = []
            if res.boxes is not None and len(res.boxes):
                xyxyn = res.boxes.xyxyn.cpu().numpy()  # normalized 0..1
                confs = res.boxes.conf.cpu().numpy()
                clss = res.boxes.cls.cpu().numpy().astype(int)
                for (x1, y1, x2, y2), c, k in zip(xyxyn, confs, clss):
                    dets.append([
                        int(k), round(float(c), 3),
                        round(float(x1), 4), round(float(y1), 4),
                        round(float(x2), 4), round(float(y2), 4),
                    ])
            frames.append(dets)
            total_dets += len(dets)
            if writer is not None:
                bgr = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                writer.stdin.write(draw_boxes(bgr, dets, infer_w, infer_h).tobytes())

    try:
        while True:
            buf = reader.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break  # end of decoded stream
            if frame_idx % args.stride == 0:
                frame = np.frombuffer(buf, np.uint8).reshape(infer_h, infer_w, 3)
                batch.append((frame_idx, frame))
                processed += 1
                if len(batch) == args.batch:
                    flush(batch)
                    batch = []
                if processed % 500 == 0:
                    print(f"  {processed} frames, {total_dets} detections ...", flush=True)
            frame_idx += 1
        if batch:
            flush(batch)
    finally:
        reader.stdout.close()
        reader.wait()
        if writer is not None:
            writer.stdin.close()
            writer.wait()

    if processed == 0:
        tmp_json.unlink(missing_ok=True)
        raise RuntimeError("decoded 0 frames")

    payload = {
        "video": src.name,
        "model": args.model,
        "width": src_w,
        "height": src_h,
        "fps": fps,
        "stride": args.stride,
        "frames_total": nb_frames,
        "frames_processed": processed,
        "classes": {str(k): v for k, v in KEEP_CLASSES.items()},
        "coords": "normalized_xyxy",
        # frames[i] holds detections for the i-th *processed* frame; multiply the
        # index by `stride` to recover the source frame number.
        "frames": frames,
    }
    tmp_json.write_text(json.dumps(payload), encoding="utf-8")
    tmp_json.replace(out_json)

    if nb_frames and processed * args.stride < COMPLETE_FRAC * nb_frames:
        print(f"WARNING: only {processed * args.stride}/{nb_frames} source frames decoded "
              f"(source may be truncated).", flush=True)
    print(f"Done: {processed} frames, {total_dets} detections -> {out_json.name}", flush=True)


def write_manifest():
    """Regenerate detections/manifest.json from the JSON files on disk."""
    stems = sorted(
        p.name[: -len(".detections.json")]
        for p in DETECT_DIR.glob("*.detections.json")
        if (STITCHED_DIR / (p.name[: -len(".detections.json")] + ".mp4")).exists()
    )
    (DETECT_DIR / "manifest.json").write_text(
        json.dumps({"videos": stems}, indent=2), encoding="utf-8"
    )
    return stems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*", help="source .mp4 path(s)")
    ap.add_argument("--all", action="store_true",
                    help="process every top-level stitched/*.mp4, smallest first")
    ap.add_argument("--force", action="store_true", help="re-run even if JSON exists")
    ap.add_argument("--render", action="store_true",
                    help="also write an annotated preview mp4 per video")
    ap.add_argument("--model", default="yolo26n.pt",
                    help="YOLO26 weights (yolo26n/s/m/l/x.pt); downloads on first use")
    ap.add_argument("--device", default="0",
                    help="'0' for first GPU, or 'cpu'")
    ap.add_argument("--imgsz", type=int, default=640, help="YOLO inference size")
    ap.add_argument("--conf", type=float, default=0.35, help="confidence threshold")
    ap.add_argument("--width", type=int, default=1280,
                    help="ffmpeg decode width fed to the model")
    ap.add_argument("--batch", type=int, default=16, help="frames per inference batch")
    ap.add_argument("--stride", type=int, default=1,
                    help="run detection every Nth frame (1 = every frame)")
    args = ap.parse_args()

    # torch's .to() needs a full device string ('cuda:0'), not a bare index '0'.
    if args.device.isdigit():
        args.device = f"cuda:{args.device}"

    if args.all:
        files = sorted(
            (f for f in STITCHED_DIR.glob("*.mp4") if not f.name.endswith(".part.mp4")),
            key=lambda f: f.stat().st_size,
        )
    else:
        if not args.videos:
            sys.exit("give one or more video paths, or --all")
        files = [Path(v) for v in args.videos]
        missing = [f for f in files if not f.exists()]
        if missing:
            sys.exit("not found: " + ", ".join(str(m) for m in missing))

    DETECT_DIR.mkdir(exist_ok=True)
    write_manifest()

    todo = []
    for f in files:
        out_json = DETECT_DIR / f"{f.stem}.detections.json"
        if not args.force and output_is_complete(f, out_json):
            print(f"skip (already detected): {f.name}", flush=True)
        else:
            todo.append(f)
    if not todo:
        print("Nothing to do.")
        return

    total_gb = sum(f.stat().st_size for f in todo) / 1e9
    print(f"\n{len(todo)} video(s) to process ({total_gb:.1f} GB of source):", flush=True)
    for f in todo:
        print(f"  {f.name}", flush=True)

    model = load_model(args.model, args.device)

    ok = failed = 0
    for i, f in enumerate(todo, 1):
        print(f"\n[{i}/{len(todo)}] {f.name}", flush=True)
        try:
            process_video(f, model, args)
            ok += 1
        except Exception as e:
            print(f"FAILED: {f.name}: {str(e)[:300]}", flush=True)
            failed += 1
        write_manifest()

    stems = write_manifest()
    print(f"\nBatch complete: {ok} processed, {failed} failed. "
          f"{len(stems)} video(s) have detections.", flush=True)


if __name__ == "__main__":
    main()
