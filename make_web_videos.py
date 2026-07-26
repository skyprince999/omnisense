"""Transcode the 1080p @ ~12 Mbps stitched videos to 720p @ ~2 Mbps for streaming.

The public viewer plays the original and its depth map at the same time. At the
source bitrate that is ~12.6 Mbps sustained per viewer, which a residential
uplink cannot hold for more than one or two people. The "Pune to Velhe" set is
already 720p @ 2 Mbps and streams fine — this brings everything else in line.

Writes to `web/<stem>.mp4`, leaving `stitched/` untouched. `serve_public.py`
serves `web/<stem>.mp4` in place of `stitched/<stem>.mp4` when it exists, so
nothing in the viewer changes. Sources already at or below TARGET_H are skipped
(the server falls back to the original for those).

Frame rate and frame count are preserved exactly: detections/tracks/distances
index by frame number (`frames[i]` -> source frame `i * stride`), so any frame
drop or fps change would desync the overlays. Coordinates are normalized 0..1,
so the resolution change itself is safe.

Usage:
    python make_web_videos.py --all            # every oversized stitched/*.mp4, smallest first
    python make_web_videos.py --all --dry-run  # show the plan only
    python make_web_videos.py "<file>.mp4"     # one file
    python make_web_videos.py --all --force    # re-encode even if already done
    python make_web_videos.py --all --cpu      # force libx264 instead of NVENC
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "stitched"
OUT_DIR = ROOT / "web"

TARGET_H = 720          # downscale anything taller; width follows the aspect ratio
TARGET_MBPS = 2.0       # average bitrate target
MAX_MBPS = 3.0          # cap for high-motion stretches
COMPLETE_FRAC = 0.98    # an output counts as done only at >=98% of source frames


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path, entries, stream=False):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", "v:0"]
    cmd += ["-show_entries", f"{'stream' if stream else 'format'}={entries}",
            "-of", "default=nw=1:nk=1", str(path)]
    r = run(cmd)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def frame_count(path):
    """Decoded frame count. -count_frames is exact but slow; the nb_frames tag is
    used first and only falls back to counting when the container omits it."""
    vals = probe(path, "nb_frames", stream=True)
    if vals and vals[0].isdigit() and int(vals[0]) > 0:
        return int(vals[0])
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
             "-show_entries", "stream=nb_read_frames", "-of", "default=nw=1:nk=1", str(path)])
    out = r.stdout.strip()
    return int(out) if out.isdigit() else 0


def video_info(path):
    vals = probe(path, "width,height", stream=True)
    if len(vals) < 2:
        return None
    return int(vals[0]), int(vals[1])


def has_nvenc():
    r = run(["ffmpeg", "-hide_banner", "-encoders"])
    return "h264_nvenc" in r.stdout


def encoder_args(use_gpu):
    if use_gpu:
        return [
            "-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq",
            "-rc", "vbr", "-cq", "30",
            "-b:v", f"{TARGET_MBPS}M", "-maxrate", f"{MAX_MBPS}M",
            "-bufsize", f"{MAX_MBPS * 2}M",
        ]
    return [
        "-c:v", "libx264", "-preset", "medium", "-crf", "26",
        "-maxrate", f"{MAX_MBPS}M", "-bufsize", f"{MAX_MBPS * 2}M",
    ]


def is_done(src, out):
    if not out.exists():
        return False
    want = frame_count(src)
    got = frame_count(out)
    return want > 0 and got >= want * COMPLETE_FRAC


def transcode(src, out, use_gpu):
    part = out.with_suffix(".part.mp4")
    if part.exists():
        part.unlink()
    cmd = (["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
            "-vf", f"scale=-2:{TARGET_H}"]
           + encoder_args(use_gpu)
           + ["-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(part)])
    r = subprocess.run(cmd)
    if r.returncode != 0 or not part.exists():
        if part.exists():
            part.unlink()
        return False, "ffmpeg failed"

    want, got = frame_count(src), frame_count(part)
    if want > 0 and got < want * COMPLETE_FRAC:
        part.unlink()
        return False, f"truncated: {got}/{want} frames"

    part.replace(out)          # atomic: never leaves a partial file looking complete
    return True, f"{got}/{want} frames"


def write_manifest():
    """Lets the server (and any later tooling) see what has been optimized."""
    stems = sorted(p.stem for p in OUT_DIR.glob("*.mp4") if not p.name.endswith(".part.mp4"))
    (OUT_DIR / "manifest.json").write_text(
        json.dumps({"videos": stems}, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="a single stitched/*.mp4 (name or path)")
    ap.add_argument("--all", action="store_true", help="every oversized stitched/*.mp4")
    ap.add_argument("--force", action="store_true", help="re-encode even if done")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cpu", action="store_true", help="use libx264 instead of NVENC")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg/ffprobe not on PATH")
    if not args.all and not args.file:
        sys.exit("give a filename or --all")

    OUT_DIR.mkdir(exist_ok=True)
    use_gpu = has_nvenc() and not args.cpu
    print(f"encoder: {'h264_nvenc (GPU)' if use_gpu else 'libx264 (CPU)'}")

    if args.all:
        srcs = sorted(SRC_DIR.glob("*.mp4"), key=lambda p: p.stat().st_size)
    else:
        p = Path(args.file)
        srcs = [p if p.is_absolute() else SRC_DIR / p.name]

    todo = []
    for src in srcs:
        info = video_info(src)
        if not info:
            print(f"  skip (unreadable): {src.name}")
            continue
        w, h = info
        if h <= TARGET_H:
            continue                      # already small enough; server uses the original
        out = OUT_DIR / src.name
        if not args.force and is_done(src, out):
            print(f"  done already: {src.name}")
            continue
        todo.append((src, out, w, h))

    total_mb = sum(s.stat().st_size for s, _, _, _ in todo) / (1 << 20)
    print(f"\n{len(todo)} file(s) to transcode, {total_mb:,.0f} MB of source\n")
    if args.dry_run:
        for src, _, w, h in todo:
            print(f"  {w}x{h}  {src.stat().st_size / (1 << 20):8,.0f} MB  {src.name}")
        return

    ok = fail = 0
    for i, (src, out, w, h) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {src.name}  ({w}x{h} -> {TARGET_H}p) ... ", end="", flush=True)
        good, msg = transcode(src, out, use_gpu)
        if good:
            before = src.stat().st_size / (1 << 20)
            after = out.stat().st_size / (1 << 20)
            print(f"ok  {before:,.0f} -> {after:,.0f} MB  ({msg})")
            ok += 1
        else:
            print(f"FAILED ({msg})")
            fail += 1
        write_manifest()                  # refresh after each file, like the other batch scripts

    print(f"\ndone: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
