"""Assign stable track IDs to the existing YOLO detections — no GPU / no re-detect.

make_detections.py runs YOLO in detect-only mode, so its boxes have no identity
across frames. The driving-skill metrics (following distance over time, closing
speed, TTC) need per-object continuity, so this stage links boxes frame-to-frame
with a lightweight greedy IoU tracker that reads the detections JSON directly.

Input : detections/<stem>.detections.json
Output: tracks/<stem>.tracks.json  — same per-processed-frame / normalized layout
        as detections, but every box gains a leading track_id:
            [track_id, cls, conf, x1n, y1n, x2n, y2n]
        plus a top-level "tracks" summary (class, first/last processed frame, count).

The join key convention is unchanged: frames[i] is the i-th *processed* frame;
the source frame number is i * stride.

Usage:
    python make_tracks.py "detections/<stem>.detections.json"   # one clip
    python make_tracks.py --all                                 # every detections JSON
    python make_tracks.py --all --force                         # re-run even if output exists
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
DETECT_DIR = BASE_DIR / "detections"
TRACKS_DIR = BASE_DIR / "tracks"

IOU_GATE = 0.30       # min IoU to link a box to an existing track (same class)
MAX_COAST = 12        # processed frames a track may go unmatched before it retires


def iou(a, b):
    """IoU of two normalized xyxy boxes."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def track_detections(frames):
    """frames: list (per processed frame) of [cls, conf, x1, y1, x2, y2] boxes.
    Returns (out_frames, summary) where out_frames prepend a track_id to each box."""
    active = []        # dicts: {id, cls, bbox, missed}
    next_id = 0
    out_frames = []
    summary = {}       # id -> {cls, first, last, count}

    for fi, boxes in enumerate(frames):
        # Candidate matches (track, box) sorted by IoU, same class only.
        pairs = []
        for ti, tr in enumerate(active):
            for bi, box in enumerate(boxes):
                if box[0] != tr["cls"]:
                    continue
                score = iou(tr["bbox"], box[2:6])
                if score >= IOU_GATE:
                    pairs.append((score, ti, bi))
        pairs.sort(reverse=True)

        matched_tracks, matched_boxes = set(), set()
        box_to_track = {}
        for score, ti, bi in pairs:
            if ti in matched_tracks or bi in matched_boxes:
                continue
            matched_tracks.add(ti)
            matched_boxes.add(bi)
            box_to_track[bi] = active[ti]["id"]
            active[ti]["bbox"] = boxes[bi][2:6]
            active[ti]["missed"] = 0

        # Unmatched boxes spawn new tracks.
        for bi, box in enumerate(boxes):
            if bi in matched_boxes:
                continue
            tid = next_id
            next_id += 1
            active.append({"id": tid, "cls": box[0], "bbox": box[2:6], "missed": 0})
            box_to_track[bi] = tid

        # Emit this frame's boxes with their track ids, in the original order.
        out_boxes = []
        for bi, box in enumerate(boxes):
            tid = box_to_track[bi]
            out_boxes.append([tid, box[0], box[1], box[2], box[3], box[4], box[5]])
            s = summary.get(tid)
            if s is None:
                summary[tid] = {"cls": box[0], "first": fi, "last": fi, "count": 1}
            else:
                s["last"] = fi
                s["count"] += 1
        out_frames.append(out_boxes)

        # Age / retire tracks that went unmatched this frame.
        for ti, tr in enumerate(active):
            if ti not in matched_tracks:
                tr["missed"] += 1
        active = [tr for tr in active if tr["missed"] <= MAX_COAST]

    return out_frames, summary


def write_manifest():
    """Regenerate tracks/manifest.json from the JSON files on disk."""
    stems = sorted(p.name[: -len(".tracks.json")] for p in TRACKS_DIR.glob("*.tracks.json"))
    (TRACKS_DIR / "manifest.json").write_text(
        json.dumps({"videos": stems}, indent=2), encoding="utf-8"
    )
    return stems


def process(det_path, force=False):
    stem = det_path.name[: -len(".detections.json")]
    out_path = TRACKS_DIR / f"{stem}.tracks.json"
    tmp_path = TRACKS_DIR / f"{stem}.tracks.part.json"
    if out_path.exists() and not force:
        print(f"skip (already tracked): {stem}", flush=True)
        return

    det = json.loads(det_path.read_text(encoding="utf-8"))
    out_frames, summary = track_detections(det["frames"])

    payload = {
        "video": det.get("video"),
        "source": det_path.name,
        "width": det.get("width"),
        "height": det.get("height"),
        "fps": det.get("fps"),
        "stride": det.get("stride", 1),
        "frames_processed": det.get("frames_processed", len(out_frames)),
        "classes": det.get("classes"),
        "coords": "normalized_xyxy",
        "iou_gate": IOU_GATE,
        "max_coast": MAX_COAST,
        # frames[i] holds tracked boxes for the i-th *processed* frame;
        # box = [track_id, cls, conf, x1n, y1n, x2n, y2n].
        "frames": out_frames,
        "tracks": {str(k): v for k, v in sorted(summary.items())},
    }
    tmp_path.write_text(json.dumps(payload), encoding="utf-8")
    tmp_path.replace(out_path)
    print(f"Done: {len(summary)} tracks over {len(out_frames)} frames -> {out_path.name}",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("detections", nargs="*", help="detections/<stem>.detections.json path(s)")
    ap.add_argument("--all", action="store_true", help="process every detections JSON")
    ap.add_argument("--force", action="store_true", help="re-run even if output exists")
    args = ap.parse_args()

    if args.all:
        files = sorted(DETECT_DIR.glob("*.detections.json"))
    else:
        if not args.detections:
            sys.exit("give one or more detections JSON paths, or --all")
        files = [Path(p) for p in args.detections]
        missing = [f for f in files if not f.exists()]
        if missing:
            sys.exit("not found: " + ", ".join(str(m) for m in missing))

    if not files:
        sys.exit("no detections JSON found in detections/")

    TRACKS_DIR.mkdir(exist_ok=True)
    for f in files:
        process(f, force=args.force)
    stems = write_manifest()
    print(f"\n{len(stems)} clip(s) have tracks.", flush=True)


if __name__ == "__main__":
    main()
