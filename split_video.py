"""Split large video files into ~equal-size parts, losslessly (no re-encode).

Part duration is computed from the file's average bitrate so each part lands
near the target size (default 500 MB). Cuts happen on keyframes, so actual
sizes vary a little. A sidecar <name>.parts.json records each part's start
offset within the original video, for mapping part timestamps back to trip time.

Usage:
    python split_video.py "stitched\\Nigdi to Yerwada [2026-06-25 1447-1522] (silent).mp4"
    python split_video.py video1.mp4 video2.mp4 --target-mb 500
    python split_video.py big.mp4 --outdir "stitched\\parts" --dry-run

Parts are written to <outdir>/<video name>/ as:
    <video name> (part 1 of 7) [+0h00m].mp4
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def split_file(path, target_mb, outdir, dry_run):
    path = Path(path)
    if not path.is_file():
        print(f"!! not found, skipping: {path}")
        return

    size_mb = path.stat().st_size / 1e6
    duration = probe_duration(path)
    if size_mb <= target_mb:
        print(f"-- {path.name}: {size_mb:.0f} MB, already under {target_mb} MB — no split needed")
        return

    bitrate_mb_s = size_mb / duration
    seg_time = int(target_mb / bitrate_mb_s)
    n_parts_est = int(size_mb / target_mb) + 1
    print(f">> {path.name}: {size_mb:.0f} MB, {duration/60:.0f} min "
          f"-> ~{n_parts_est} parts of ~{seg_time//60}m{seg_time%60:02d}s each")
    if dry_run:
        return

    part_dir = Path(outdir) / path.stem if outdir else path.parent / f"{path.stem} parts"
    part_dir.mkdir(parents=True, exist_ok=True)
    pattern = part_dir / "raw_part_%03d.mp4"

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(path), "-c", "copy", "-map", "0",
         "-f", "segment", "-segment_time", str(seg_time),
         "-reset_timestamps", "1", str(pattern)],
        check=True,
    )

    raw_parts = sorted(part_dir.glob("raw_part_*.mp4"))
    total = len(raw_parts)
    offset = 0.0
    manifest = []
    for i, raw in enumerate(raw_parts, start=1):
        part_dur = probe_duration(raw)
        h, m = int(offset // 3600), int(offset % 3600 // 60)
        final = part_dir / f"{path.stem} (part {i} of {total}) [+{h}h{m:02d}m].mp4"
        raw.rename(final)
        manifest.append({
            "part": i,
            "of": total,
            "file": final.name,
            "start_offset_s": round(offset, 1),
            "duration_s": round(part_dur, 1),
            "size_mb": round(final.stat().st_size / 1e6),
        })
        print(f"   part {i}/{total}: {manifest[-1]['size_mb']} MB, "
              f"starts at +{h}h{m:02d}m, {part_dur/60:.1f} min")
        offset += part_dur

    sidecar = part_dir / f"{path.stem}.parts.json"
    sidecar.write_text(json.dumps(
        {"source": path.name, "total_duration_s": round(duration, 1), "parts": manifest},
        indent=2))
    print(f"   -> {total} parts in {part_dir}")
    print(f"   -> offsets saved to {sidecar.name}")


def main():
    ap = argparse.ArgumentParser(description="Losslessly split videos into ~equal-size parts.")
    ap.add_argument("files", nargs="+", help="video file(s) to split")
    ap.add_argument("--target-mb", type=int, default=500, help="target part size in MB (default 500)")
    ap.add_argument("--outdir", help="parent folder for part folders (default: next to each input)")
    ap.add_argument("--dry-run", action="store_true", help="show the split plan without splitting")
    args = ap.parse_args()

    for f in args.files:
        try:
            split_file(f, args.target_mb, args.outdir, args.dry_run)
        except subprocess.CalledProcessError as e:
            print(f"!! ffmpeg/ffprobe failed on {f}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
