"""Stitch each subfolder of PNG frames in the Clean_Ego_Dataset into an mp4.

The dataset lays out one crash/driving clip per subfolder, with the frames named
by their time order (e.g. 0240.png ... 0321.png). This walks every subfolder of
each root, feeds the frames to ffmpeg in sorted order, and writes one
browser-playable H.264 mp4 per subfolder into the output directory.

Frames are piped to ffmpeg over stdin (image2pipe) rather than matched with an
image2 filename pattern, so the numbering can start anywhere, use any padding,
and have gaps without breaking the run.

Like the other batch scripts here it is idempotent and resumable: output goes to
a `.part.mp4` that is atomically renamed on success, and a clip counts as done
only if the encoded frame count covers >= COMPLETE_FRAC of its source frames.

Usage:
    python stitch_ego_frames.py --dry-run          # show the plan, encode nothing
    python stitch_ego_frames.py                    # default root: 1_Ego_Fault
    python stitch_ego_frames.py --all-roots        # all three top-level dataset folders
    python stitch_ego_frames.py --fps 15 --workers 6
    python stitch_ego_frames.py --force            # re-encode clips that are already done
    python stitch_ego_frames.py "<some/other/root>" --out "<dir>"

Requires: ffmpeg and ffprobe on PATH.
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATASET_DIR = Path(r"C:\Users\ADMIN\Downloads\archive\Clean_Ego_Dataset")
DEFAULT_ROOT = DATASET_DIR / "1_Ego_Fault"
ALL_ROOTS = [
    DATASET_DIR / "1_Ego_Fault",
    DATASET_DIR / "0_Non_Ego_Fault",
    DATASET_DIR / "0_Normal_Driving",
]
# Videos land in Clean_Ego_Dataset/videos/<root name>/ unless --out says otherwise.
DEFAULT_OUT_ROOT = DATASET_DIR / "videos"

FRAME_EXTS = (".png", ".jpg", ".jpeg")
DEFAULT_FPS = 10          # these clips are ~10 fps dashcam captures
COMPLETE_FRAC = 0.98      # an mp4 counts as done at >= 98% of its source frames
CRF = 20


def frame_sort_key(path):
    """Sort numerically when the stem is a number, else lexicographically.

    Returns a tuple so the two cases never compare against each other.
    """
    stem = path.stem
    if stem.isdigit():
        return (0, int(stem), stem)
    return (1, 0, stem)


def list_frames(folder):
    frames = [p for p in folder.iterdir()
              if p.is_file() and p.suffix.lower() in FRAME_EXTS]
    frames.sort(key=frame_sort_key)
    return frames


def encoded_frame_count(mp4):
    """Frame count of an existing mp4, or 0 if it is missing/unreadable."""
    if not mp4.exists():
        return 0
    for args in (
        ["-show_entries", "stream=nb_frames"],
        ["-count_frames", "-show_entries", "stream=nb_read_frames"],
    ):
        try:
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 *args, "-of", "csv=p=0", str(mp4)],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 0
        if out.isdigit() and int(out) > 0:
            return int(out)
    return 0


def is_done(mp4, n_frames):
    return encoded_frame_count(mp4) >= n_frames * COMPLETE_FRAC


def encode(frames, out_mp4, fps):
    """Pipe `frames` into ffmpeg and write out_mp4 atomically. Returns (ok, msg)."""
    part = out_mp4.with_suffix(".part.mp4")
    part.unlink(missing_ok=True)

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
        # yuv420p needs even dimensions; the source is already even but padding
        # here keeps odd-sized clips from failing the whole run.
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(CRF),
        "-preset", "medium", "-movflags", "+faststart",
        "-r", str(fps),
        str(part),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for frame in frames:
            proc.stdin.write(frame.read_bytes())
        proc.stdin.close()
    except (BrokenPipeError, OSError):
        pass  # ffmpeg died early; the stderr below explains why
    stderr = proc.communicate()[1].decode("utf-8", "replace").strip()

    if proc.returncode != 0 or not part.exists():
        part.unlink(missing_ok=True)
        return False, stderr or f"ffmpeg exited {proc.returncode}"

    if not is_done(part, len(frames)):
        got = encoded_frame_count(part)
        part.unlink(missing_ok=True)
        return False, f"truncated: {got}/{len(frames)} frames encoded"

    part.replace(out_mp4)
    return True, ""


def plan_root(root, out_dir, force):
    """Build the per-subfolder job list for one root. Returns (jobs, skipped, empty)."""
    jobs, skipped, empty = [], [], []
    out_resolved = out_dir.resolve()
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        if folder.resolve() == out_resolved:
            continue  # writing videos inside the root shouldn't feed them back in
        frames = list_frames(folder)
        if not frames:
            empty.append(folder.name)
            continue
        out_mp4 = out_dir / f"{folder.name}.mp4"
        if not force and is_done(out_mp4, len(frames)):
            skipped.append(folder.name)
            continue
        jobs.append((folder, frames, out_mp4))
    # Smallest first, matching the other batch scripts: quick wins land early.
    jobs.sort(key=lambda job: len(job[1]))
    return jobs, skipped, empty


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roots", nargs="*", type=Path,
                    help=f"dataset folders to walk (default: {DEFAULT_ROOT.name})")
    ap.add_argument("--all-roots", action="store_true",
                    help="process all three top-level Clean_Ego_Dataset folders")
    ap.add_argument("--out", type=Path,
                    help="output directory (default: <dataset>/videos/<root name>/)")
    ap.add_argument("--fps", type=int, default=DEFAULT_FPS,
                    help=f"playback frame rate (default: {DEFAULT_FPS})")
    ap.add_argument("--workers", type=int, default=4,
                    help="parallel ffmpeg encodes (default: 4)")
    ap.add_argument("--force", action="store_true",
                    help="re-encode clips that already have a complete mp4")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and exit without encoding")
    args = ap.parse_args()

    if args.all_roots:
        roots = ALL_ROOTS
    elif args.roots:
        roots = args.roots
    else:
        roots = [DEFAULT_ROOT]

    missing = [r for r in roots if not r.is_dir()]
    if missing:
        for r in missing:
            print(f"error: not a directory: {r}", file=sys.stderr)
        return 1
    if args.out and len(roots) > 1:
        print("error: --out takes a single root; drop it to use the default layout",
              file=sys.stderr)
        return 1

    failures = []
    for root in roots:
        out_dir = args.out or (DEFAULT_OUT_ROOT / root.name)
        jobs, skipped, empty = plan_root(root, out_dir, args.force)

        total_frames = sum(len(f) for _, f, _ in jobs)
        print(f"\n{root}")
        print(f"  -> {out_dir}")
        print(f"  {len(jobs)} to encode ({total_frames} frames), "
              f"{len(skipped)} already done, {len(empty)} with no frames")
        if empty:
            print(f"  no frames in: {', '.join(empty[:5])}"
                  + (f" (+{len(empty) - 5} more)" if len(empty) > 5 else ""))

        if args.dry_run:
            for folder, frames, out_mp4 in jobs[:10]:
                secs = len(frames) / args.fps
                print(f"    {folder.name}: {len(frames)} frames -> "
                      f"{out_mp4.name} ({secs:.1f}s @ {args.fps}fps)")
            if len(jobs) > 10:
                print(f"    ... {len(jobs) - 10} more")
            continue
        if not jobs:
            continue

        out_dir.mkdir(parents=True, exist_ok=True)
        done = 0

        def run(job):
            folder, frames, out_mp4 = job
            ok, msg = encode(frames, out_mp4, args.fps)
            return folder.name, len(frames), ok, msg

        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            for name, n, ok, msg in pool.map(run, jobs):
                done += 1
                if ok:
                    print(f"  [{done}/{len(jobs)}] {name}: {n} frames -> ok")
                else:
                    failures.append(f"{root.name}/{name}: {msg}")
                    print(f"  [{done}/{len(jobs)}] {name}: FAILED - {msg}")

    if failures:
        print(f"\n{len(failures)} failed:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
