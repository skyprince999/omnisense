"""Stitch 1-minute dashcam clips into per-trip videos and upload to VideoDB.

Clip filenames follow YYYYMMDDHHMMSS_0060.mp4 (start timestamp + duration in
seconds). Clips are grouped into contiguous segments — a new segment starts
whenever the gap between one clip's end and the next clip's start exceeds
GAP_TOLERANCE_S — then each segment is concatenated with ffmpeg stream copy
(no re-encode) and uploaded + scene-indexed on VideoDB.

Usage:
    python stitch_and_upload.py --dry-run      # show the segment plan only
    python stitch_and_upload.py --stitch-only  # stitch, skip upload/index
    python stitch_and_upload.py                # stitch + upload + index

State is tracked in stitched/manifest.json; completed steps are skipped on
re-run, so the script is safe to interrupt and restart.

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
STITCHED_DIR = BASE_DIR / "Nagar highway trip" #"stitched"
MANIFEST_PATH = STITCHED_DIR / "manifest.json"

TRIP_FOLDERS = [
    "VN to PIC Pashan",
    "Nigdi to Yerwada",
    "Car Dashcam",
    "Good videos",
    "Nagar highway trip",
]

CLIP_RE = re.compile(r"^(\d{14})_(\d{4})\.mp4$", re.IGNORECASE)

# A clip nominally ends at start + duration; allow this much slack before
# declaring a gap and starting a new segment.
GAP_TOLERANCE_S = 60

SCENE_PROMPT = (
    "This is dashcam footage from a car driving in India. Describe: road type "
    "(highway/urban street/rural road/ghat section), traffic density and the "
    "types of vehicles visible (cars, trucks, buses, two-wheelers, autos), "
    "weather and visibility, lighting (day/dusk/night), road surface condition "
    "(potholes, construction, waterlogging), and any notable events: hard "
    "braking, close following, risky overtakes, pedestrians or animals on the "
    "road, near misses, toll plazas, traffic signals, or unusual obstacles. "
    "Mention visible landmarks, signboards, or place names if readable."
)


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def scan_segments():
    """Return a list of segment dicts across all trip folders."""
    segments = []
    for folder in TRIP_FOLDERS:
        folder_path = BASE_DIR / folder
        if not folder_path.is_dir():
            print(f"  !! folder not found, skipping: {folder}")
            continue
        clips = []
        for f in sorted(folder_path.rglob("*.mp4")):
            m = CLIP_RE.match(f.name)
            if not m:
                print(f"  !! unrecognized filename, skipping: {folder}/{f.name}")
                continue
            start = datetime.strptime(m.group(1), "%Y%m%d%H%M%S")
            duration = int(m.group(2))
            clips.append({"path": f, "start": start, "duration": duration})
        clips.sort(key=lambda c: c["start"])

        current = []
        for clip in clips:
            if current:
                prev = current[-1]
                expected_next = prev["start"] + timedelta(
                    seconds=prev["duration"] + GAP_TOLERANCE_S
                )
                if clip["start"] > expected_next:
                    segments.append(make_segment(folder, current))
                    current = []
            current.append(clip)
        if current:
            segments.append(make_segment(folder, current))
    return segments


def make_segment(folder, clips):
    start = clips[0]["start"]
    end = clips[-1]["start"] + timedelta(seconds=clips[-1]["duration"])
    name = f"{folder} [{start:%Y-%m-%d %H%M}-{end:%H%M}]"
    return {
        "id": name,
        "folder": folder,
        "name": name,
        "start": start,
        "end": end,
        "clips": clips,
        "output": STITCHED_DIR / f"{name}.mp4",
    }


def load_manifest():
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def save_manifest(manifest):
    STITCHED_DIR.mkdir(exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, default=str))


def stitch(segment):
    STITCHED_DIR.mkdir(exist_ok=True)
    out = segment["output"]
    if out.exists() and out.stat().st_size > 0:
        return
    list_file = STITCHED_DIR / "concat_list.txt"
    lines = []
    for clip in segment["clips"]:
        p = str(clip["path"]).replace("'", "'\\''")
        lines.append(f"file '{p}'")
    list_file.write_text("\n".join(lines), encoding="utf-8")
    tmp = out.with_suffix(".part.mp4")
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy", str(tmp),
    ]
    subprocess.run(cmd, check=True)
    tmp.replace(out)
    list_file.unlink(missing_ok=True)


def scene_index_status(video, index_id):
    """Return 'done', 'failed', or 'running' for a scene index."""
    for idx in video.list_scene_index():
        if idx.get("scene_index_id") == index_id:
            status = idx.get("status", "")
            if status == "failed":
                return "failed"
            if status in ("done", "completed", "success"):
                return "done"
            return "running"
    return "failed"


def upload_segment(segment, manifest, coll):
    entry = manifest.setdefault(segment["id"], {})
    if entry.get("video_id"):
        print(f"    already uploaded: video_id={entry['video_id']}")
        return
    print(f"    uploading ({segment['output'].stat().st_size / 1e6:.0f} MB)...")
    video = coll.upload(file_path=str(segment["output"]), name=segment["name"])
    entry["video_id"] = video.id
    save_manifest(manifest)
    print(f"    uploaded: video_id={video.id}")


def index_segment(segment, manifest, coll):
    """Create/retry scene index. Returns True if index is done or running."""
    from videodb import SceneExtractionType

    entry = manifest.setdefault(segment["id"], {})
    if not entry.get("video_id"):
        print("    not uploaded yet, skipping index")
        return False
    video = coll.get_video(entry["video_id"])

    if entry.get("scene_index_id"):
        status = scene_index_status(video, entry["scene_index_id"])
        if status == "done":
            print(f"    index done: {entry['scene_index_id']}")
            return True
        if status == "running":
            print(f"    index still running: {entry['scene_index_id']}")
            return True
        print(f"    previous index failed ({entry['scene_index_id']}), retrying...")
        entry["scene_index_id"] = None

    try:
        index_id = video.index_scenes(
            extraction_type=SceneExtractionType.time_based,
            extraction_config={"time": 10, "select_frames": ["first"]},
            prompt=SCENE_PROMPT,
            name=f"dashcam-index {segment['name']}",
        )
    except Exception as e:
        print(f"    index request failed: {str(e)[:150]}")
        return False
    status = scene_index_status(video, index_id)
    if status == "failed":
        print(f"    scene index FAILED server-side: {index_id}")
        return False
    entry["scene_index_id"] = index_id
    save_manifest(manifest)
    print(f"    scene index created: {index_id} ({status})")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="show segment plan only")
    ap.add_argument("--stitch-only", action="store_true", help="stitch, skip upload")
    ap.add_argument("--skip-index", action="store_true", help="upload but don't scene-index")
    ap.add_argument("--index-only", action="store_true", help="only (re)try scene indexing")
    ap.add_argument("--only", help="process only segments whose name contains this substring")
    args = ap.parse_args()

    load_env()
    segments = scan_segments()
    if args.only:
        segments = [s for s in segments if args.only.lower() in s["name"].lower()]

    print(f"\nSegment plan ({len(segments)} segments):\n")
    for seg in segments:
        mins = (seg["end"] - seg["start"]).total_seconds() / 60
        mb = sum(c["path"].stat().st_size for c in seg["clips"]) / 1e6
        print(f"  {seg['name']}")
        print(f"      {len(seg['clips'])} clips, {mins:.0f} min, {mb:.0f} MB")
    if args.dry_run:
        return

    if not args.index_only:
        print("\nStitching...")
        for seg in segments:
            if seg["output"].exists() and seg["output"].stat().st_size > 0:
                print(f"  already stitched: {seg['output'].name}")
            else:
                print(f"  stitching {seg['output'].name} ...")
                stitch(seg)
        print("Stitching done.")

        if args.stitch_only:
            return

    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit(
            "\nVIDEODB_API_KEY is not set. Set it in the environment or in a "
            ".env file next to this script, then re-run to upload."
        )

    from videodb import connect

    conn = connect(api_key=api_key)
    coll = conn.get_collection()
    manifest = load_manifest()

    if not args.index_only:
        print("\nUploading...")
        for seg in segments:
            print(f"  {seg['name']}")
            upload_segment(seg, manifest, coll)

    if not args.skip_index:
        print("\nScene indexing...")
        ok = failed = 0
        for seg in segments:
            print(f"  {seg['name']}")
            if index_segment(seg, manifest, coll):
                ok += 1
            else:
                failed += 1
        print(f"\nIndexing: {ok} ok/running, {failed} failed.")
        if failed:
            print("Re-run with --index-only to retry failed indexes later.")

    print("Manifest: " + str(MANIFEST_PATH))


if __name__ == "__main__":
    main()
