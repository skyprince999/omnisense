"""Render depth-perception videos for dashcam clips using Depth Anything V2.

Decodes each source video with ffmpeg (robust to the corrupt/dropped frames
common in dashcam footage), runs monocular depth estimation on the GPU,
colorizes the depth map (inferno: near = bright), and encodes a new .mp4 in
depth/ with the same fps and duration. Also maintains depth/videos.js — the
manifest depth_viewer.html uses to populate its video dropdown.

Usage:
    python make_depth_video.py "stitched/<clip>.mp4"        # one video
    python make_depth_video.py --all                        # every top-level stitched/*.mp4,
                                                            # smallest first, skipping ones already done
    python make_depth_video.py --all --force                # re-render even if output exists
    python make_depth_video.py <video.mp4> --model base     # higher quality, ~3x slower

Requires: torch (CUDA), transformers, opencv-python, and ffmpeg/ffprobe on PATH.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from tqdm import tqdm

BASE_DIR = Path(__file__).parent
STITCHED_DIR = BASE_DIR / "stitched" #"Calliberation Videos" 
DEPTH_DIR = BASE_DIR / "depth" #"Calliberation Videos_depth"

MODELS = {
    "small": "depth-anything/Depth-Anything-V2-Small-hf",
    "base": "depth-anything/Depth-Anything-V2-Base-hf",
    "large": "depth-anything/Depth-Anything-V2-Large-hf",
}

# EMA factor for the running depth-range bounds. Per-frame min/max normalization
# makes the video strobe; smoothing the bounds keeps brightness stable.
EMA_ALPHA = 0.05

# An existing depth video counts as "done" only if it has at least this fraction
# of the source's frames — guards against truncated renders from earlier runs.
COMPLETE_FRAC = 0.98


def load_model(name):
    from transformers import AutoImageProcessor, AutoModelForDepthEstimation

    model_id = MODELS[name]
    print(f"Loading {model_id} ...", flush=True)
    processor = AutoImageProcessor.from_pretrained(model_id)
    model = AutoModelForDepthEstimation.from_pretrained(
        model_id, torch_dtype=torch.float16
    )
    model.to("cuda").eval()
    return processor, model


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


@torch.inference_mode()
def infer_depth_batch(frames_rgb, processor, model):
    """frames_rgb: list of HxWx3 uint8 RGB arrays -> list of HxW float32 depth maps."""
    inputs = processor(images=frames_rgb, return_tensors="pt")
    inputs = {k: v.to("cuda", torch.float16) for k, v in inputs.items()}
    depth = model(**inputs).predicted_depth  # (B, h, w)
    h, w = frames_rgb[0].shape[:2]
    depth = torch.nn.functional.interpolate(
        depth.unsqueeze(1).float(), size=(h, w), mode="bilinear", align_corners=False
    ).squeeze(1)
    return depth.cpu().numpy()


def output_is_complete(src, out):
    """True if out exists and has ~as many frames as src (not a truncated render)."""
    if not out.exists():
        return False
    try:
        _, _, _, src_n = probe_video(src)
        _, _, _, out_n = probe_video(out)
    except Exception:
        return False
    if src_n == 0:
        return out_n > 0
    return out_n >= COMPLETE_FRAC * src_n


def write_manifest():
    """Regenerate depth/videos.js from the depth videos that exist on disk."""
    stems = sorted(
        p.name[: -len(".depth.mp4")]
        for p in DEPTH_DIR.glob("*.depth.mp4")
        if (STITCHED_DIR / (p.name[: -len(".depth.mp4")] + ".mp4")).exists()
    )
    js = "window.DEPTH_VIDEOS = " + json.dumps(stems, indent=2) + ";\n"
    (DEPTH_DIR / "videos.js").write_text(js, encoding="utf-8")
    return stems


def process_video(src, processor, model, args):
    src_w, src_h, fps, nb_frames = probe_video(src)

    out_w = args.width
    out_h = int(round(src_h * out_w / src_w / 2) * 2)  # keep even for yuv420p
    infer_w = min(out_w, src_w)
    infer_h = int(round(src_h * infer_w / src_w))
    frame_bytes = infer_w * infer_h * 3

    out_path = DEPTH_DIR / f"{src.stem}.depth.mp4"
    tmp_path = DEPTH_DIR / f"{src.stem}.depth.part.mp4"

    print(f"Source: {src.name}  {src_w}x{src_h} @ {fps:.2f} fps, {nb_frames} frames", flush=True)
    reader = start_ffmpeg_reader(src, infer_w, infer_h)
    writer = start_ffmpeg_writer(tmp_path, out_w, out_h, fps)

    lo = hi = None  # EMA-smoothed depth range
    batch = []
    written = 0

    def flush(batch):
        nonlocal lo, hi, written
        for depth in infer_depth_batch(batch, processor, model):
            d_lo, d_hi = float(depth.min()), float(depth.max())
            if lo is None:
                lo, hi = d_lo, d_hi
            else:
                lo += EMA_ALPHA * (d_lo - lo)
                hi += EMA_ALPHA * (d_hi - hi)
            norm = np.clip((depth - lo) / max(hi - lo, 1e-6), 0, 1)
            gray = (norm * 255).astype(np.uint8)
            color = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
            color = cv2.resize(color, (out_w, out_h), interpolation=cv2.INTER_LINEAR)
            writer.stdin.write(color.tobytes())
            written += 1

    try:
        with tqdm(total=nb_frames or None, unit="frame", mininterval=5.0) as bar:
            while True:
                buf = reader.stdout.read(frame_bytes)
                if len(buf) < frame_bytes:
                    break  # end of decoded stream
                frame = np.frombuffer(buf, np.uint8).reshape(infer_h, infer_w, 3)
                batch.append(frame)
                if len(batch) == args.batch:
                    flush(batch)
                    bar.update(len(batch))
                    batch = []
            if batch:
                flush(batch)
                bar.update(len(batch))
    finally:
        reader.stdout.close()
        reader.wait()
        writer.stdin.close()
        writer.wait()

    if writer.returncode != 0:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg exited with code {writer.returncode}")
    if written == 0:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError("decoded 0 frames")
    tmp_path.replace(out_path)
    if nb_frames and written < COMPLETE_FRAC * nb_frames:
        print(f"WARNING: only {written}/{nb_frames} frames decoded (source may be truncated).", flush=True)
    print(f"Done: {written} frames -> {out_path.name}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*", help="source .mp4 path(s)")
    ap.add_argument("--all", action="store_true",
                    help="process every top-level stitched/*.mp4, smallest first")
    ap.add_argument("--force", action="store_true", help="re-render even if output exists")
    ap.add_argument("--model", choices=MODELS, default="base")
    ap.add_argument("--width", type=int, default=960, help="depth video output width")
    ap.add_argument("--batch", type=int, default=8, help="inference batch size")
    args = ap.parse_args()

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

    if not torch.cuda.is_available():
        sys.exit("CUDA is not available — check the torch install.")

    DEPTH_DIR.mkdir(exist_ok=True)
    write_manifest()

    todo = []
    for f in files:
        out = DEPTH_DIR / f"{f.stem}.depth.mp4"
        if not args.force and output_is_complete(f, out):
            print(f"skip (already rendered): {f.name}", flush=True)
        else:
            todo.append(f)
    if not todo:
        print("Nothing to do.")
        return

    total_gb = sum(f.stat().st_size for f in todo) / 1e9
    print(f"\n{len(todo)} video(s) to render ({total_gb:.1f} GB of source):", flush=True)
    for f in todo:
        print(f"  {f.name}", flush=True)

    processor, model = load_model(args.model)

    ok = failed = 0
    for i, f in enumerate(todo, 1):
        print(f"\n[{i}/{len(todo)}] {f.name}", flush=True)
        try:
            process_video(f, processor, model, args)
            ok += 1
        except Exception as e:
            print(f"FAILED: {f.name}: {str(e)[:300]}", flush=True)
            failed += 1
        write_manifest()

    stems = write_manifest()
    print(f"\nBatch complete: {ok} rendered, {failed} failed. "
          f"{len(stems)} video(s) in the viewer dropdown.", flush=True)


if __name__ == "__main__":
    main()
