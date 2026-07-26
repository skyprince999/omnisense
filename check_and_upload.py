"""Sync the stitched/ folder to VideoDB: list what's already uploaded, then
upload only the missing videos, one by one.

The source of truth for "already uploaded" is VideoDB itself — the script
connects, lists every video in the default collection, and compares by name
(upload name = filename without extension). No local manifest needed to resume.

Which local files count as candidates:
  - top-level stitched/*.mp4
  - mp4s inside "<video> parts" subfolders (created by split_video.py)
  - EXCLUDED: the "with audio" subfolder, *.part.mp4 temp files
  - top-level files larger than MAX_UPLOAD_MB are skipped with a warning
    (upload their parts instead — create them with split_video.py); if a
    parts folder exists for such a file, the original is skipped silently
    in favor of its parts.

Usage:
    python check_and_upload.py --dry-run   # report uploaded vs missing, no uploads
    python check_and_upload.py             # upload all missing files, one by one
    python check_and_upload.py --only pune # restrict to matching filenames
    python check_and_upload.py --strip-audio  # de-audio candidates before upload:
                                              # original moves to "with audio"/,
                                              # silent copy keeps the same name
    python check_and_upload.py --dir "Nagar highway trip"  # upload from another
                                              # folder instead of stitched/

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
STITCHED_DIR = BASE_DIR / "stitched"
EXCLUDED_SUBFOLDERS = {"with audio"}
MAX_UPLOAD_MB = 1000  # current-tier upload limit; larger files must be split first


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def gather_candidates(source_dir):
    """Return (uploadable files, oversized files that need splitting)."""
    candidates = []
    needs_split = []

    top_level = [
        f for f in sorted(source_dir.glob("*.mp4"))
        if not f.name.endswith(".part.mp4")
    ]
    for f in top_level:
        size_mb = f.stat().st_size / 1e6
        parts_dir = source_dir / f"{f.stem} parts"
        if size_mb > MAX_UPLOAD_MB:
            if not parts_dir.is_dir():
                needs_split.append(f)
            continue  # parts (if any) are picked up below; original never uploaded
        candidates.append(f)

    for sub in sorted(source_dir.iterdir()):
        if not sub.is_dir() or sub.name.lower() in EXCLUDED_SUBFOLDERS:
            continue
        candidates.extend(
            f for f in sorted(sub.glob("*.mp4"))
            if not f.name.endswith(".part.mp4")
        )

    return candidates, needs_split


def has_audio(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return bool(out.stdout.strip())


def strip_audio(path):
    """Replace path with a silent stream-copy; original moves to "with audio"/."""
    backup_dir = path.parent / "with audio"
    backup_dir.mkdir(exist_ok=True)
    tmp = path.with_suffix(".part.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(path), "-c", "copy", "-an", str(tmp)],
        check=True,
    )
    path.replace(backup_dir / path.name)
    tmp.replace(path)


def fetch_uploaded_names(coll):
    """Names of all videos already in the collection."""
    return {v.name for v in coll.get_videos()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="report uploaded vs missing without uploading")
    ap.add_argument("--only", help="only files whose name contains this substring")
    ap.add_argument("--strip-audio", action="store_true",
                    help="remove the audio track from candidates before upload "
                         '(original is kept in the "with audio" subfolder)')
    ap.add_argument("--dir", default=str(STITCHED_DIR),
                    help="folder to upload videos from (default: stitched/)")
    args = ap.parse_args()

    source_dir = Path(args.dir)
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir
    if not source_dir.is_dir():
        sys.exit(f"Source folder not found: {source_dir}")

    load_env()
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")

    candidates, needs_split = gather_candidates(source_dir)
    if args.only:
        candidates = [f for f in candidates if args.only.lower() in f.name.lower()]

    if args.strip_audio:
        with_audio = [f for f in candidates if has_audio(f)]
        print(f"Stripping audio from {len(with_audio)} of {len(candidates)} candidates...")
        for f in with_audio:
            if args.dry_run:
                print(f"  ~ would strip: {f.name}")
                continue
            strip_audio(f)
            print(f"  ~ stripped: {f.name}")

    from videodb import connect

    print("Connecting to VideoDB and listing uploaded videos...")
    conn = connect(api_key=api_key)
    coll = conn.get_collection()
    uploaded_names = fetch_uploaded_names(coll)
    print(f"  {len(uploaded_names)} videos currently in the collection")

    already = [f for f in candidates if f.stem in uploaded_names]
    missing = [f for f in candidates if f.stem not in uploaded_names]

    print(f"\nAlready uploaded ({len(already)}):")
    for f in already:
        print(f"  = {f.name}")
    print(f"\nTo upload ({len(missing)}):")
    for f in missing:
        print(f"  + {f.name}  ({f.stat().st_size / 1e6:.0f} MB)")
    for f in needs_split:
        print(f"  !! too large for current tier, split first with split_video.py: "
              f"{f.name} ({f.stat().st_size / 1e6:.0f} MB)")

    if args.dry_run or not missing:
        if not missing:
            print("\nNothing to upload.")
        return

    print("\nUploading one by one...")
    done = failed = 0
    for i, f in enumerate(missing, start=1):
        size_mb = f.stat().st_size / 1e6
        print(f"  [{i}/{len(missing)}] {f.name} ({size_mb:.0f} MB)...")
        try:
            video = coll.upload(file_path=str(f), name=f.stem)
            done += 1
            print(f"      OK  video_id={video.id}")
        except Exception as e:
            failed += 1
            print(f"      FAILED: {str(e)[:200]}")

    print(f"\nDone: {done} uploaded, {failed} failed, "
          f"{len(already)} were already up.")
    if failed:
        print("Re-run the script to retry failures — already-uploaded files are skipped.")


if __name__ == "__main__":
    main()
