"""Estimate per-object distance (and following-distance / closing-speed / TTC) from tracks.

Reads tracks/<stem>.tracks.json and, for every tracked box, computes how far the
object is from the *front of the ego car* using two of the three routes from
dashcam_distance_benchmark.md (the DA-V2 depth route is deferred — see DISTANCE_PLAN.md):

    Route A  ground-plane geometry :  Z = f_norm_y * cam_h / (v_n - v0_norm)
    Route B  known object width    :  Z = f_norm_x * class_width / (x2n - x1n)

All geometry is done in NORMALIZED coordinates so it is resolution-independent and
matches the detections/tracks schema. Camera intrinsics come from the staged slot
calibration/dashcam_calibration.json — swap in benchmark-measured values there and
distances become metric-accurate with no code change.

The two routes are fused (confidence-weighted) into Z_m, then
    gap_m = Z_m - bumper_offset_m   (distance from the front bumper to the object)

Then, per track_id, the distance-over-time series yields closing speed and TTC — the
inputs the coaching layer turns into tailgating / near-miss nudges. A second,
calibration-free TTC channel is derived from bounding-box area expansion as a
cross-check.

Input : tracks/<stem>.tracks.json  (run make_tracks.py first)
Output: distances/<stem>.distances.json
        frames[i] = [ [track_id, cls, Z_m, gap_m, conf], ... ]   (i-th processed frame)
        tracks[id] = per-object summary incl. min_gap_m, min_ttc_s, min_ttc_si_s.

Usage:
    python make_distances.py "tracks/<stem>.tracks.json"   # one clip
    python make_distances.py --all                         # every tracks JSON
    python make_distances.py --all --force                 # re-run even if output exists
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).parent
TRACKS_DIR = BASE_DIR / "tracks"
DIST_DIR = BASE_DIR / "distances"
CALIB_PATH = BASE_DIR / "calibration" / "dashcam_calibration.json"

# Distance beyond which an estimate is treated as "no reading" (unstable near the
# horizon, tiny far boxes). Objects farther than this rarely matter for coaching.
MAX_Z_M = 120.0
SMOOTH_WIN = 7        # processed-frame window (odd) for the rolling-median Z smoother
SLOPE_WIN = 9         # processed-frame window for the closing-speed line fit
MIN_CLOSING_MPS = 0.3  # ignore closing speeds below this (noise) when forming TTC


def load_calib():
    c = json.loads(CALIB_PATH.read_text(encoding="utf-8"))
    c["f_norm_x"] = c["f_px"] / c["native_width"]
    c["f_norm_y"] = c["f_px"] / c["native_height"]
    K = c["fisheye"].get("K")
    D = c["fisheye"].get("D")
    c["_K"] = np.array(K, dtype=np.float64) if K else None
    c["_D"] = np.array(D, dtype=np.float64) if D else None
    return c


def undistort_point(u_n, v_n, calib):
    """Undistort a normalized image point through the fisheye model, if calibrated.
    Returns normalized coords. No-op when K/D are absent (v1 default)."""
    if calib["_K"] is None or calib["_D"] is None:
        return u_n, v_n
    import cv2
    w, h = calib["native_width"], calib["native_height"]
    pt = np.array([[[u_n * w, v_n * h]]], dtype=np.float64)
    out = cv2.fisheye.undistortPoints(pt, calib["_K"], calib["_D"], P=calib["_K"])
    ux, uy = out[0, 0]
    return ux / w, uy / h


def estimate_box(cls_name, conf, x1, y1, x2, y2, calib):
    """Fuse the ground-plane and known-width routes for one box.
    Returns (Z_m, gap_m, fused_conf) or None if no route yields a plausible reading."""
    v0 = calib["v0_norm"]
    # Contact point = bottom-center of the box (approx tire/foot ground contact).
    uc, vc = undistort_point((x1 + x2) / 2.0, y2, calib)

    routes = []  # (Z, weight)

    # Route A: ground plane. Valid only for objects below the horizon.
    if vc > v0:
        z_g = calib["f_norm_y"] * calib["cam_h_m"] / (vc - v0)
        # Trust grows as the contact sits well below the horizon (larger, stabler denom).
        w_g = min(1.0, (vc - v0) / 0.20) * conf
        if 0 < z_g < MAX_Z_M and w_g > 0:
            routes.append((z_g, w_g))

    # Route B: known width. Undistort both horizontal edges so width is measured
    # in undistorted space when calibrated.
    ux1, _ = undistort_point(x1, (y1 + y2) / 2.0, calib)
    ux2, _ = undistort_point(x2, (y1 + y2) / 2.0, calib)
    w_n = abs(ux2 - ux1)
    W = calib["class_width_m"].get(cls_name)
    if W and w_n > 1e-4:
        z_w = calib["f_norm_x"] * W / w_n
        rel = calib.get("class_width_reliability", {}).get(cls_name, 0.5)
        w_w = rel * conf
        if 0 < z_w < MAX_Z_M and w_w > 0:
            routes.append((z_w, w_w))

    if not routes:
        return None
    wsum = sum(w for _, w in routes)
    z = sum(z * w for z, w in routes) / wsum
    gap = z - calib["bumper_offset_m"]
    # Confidence: strength of evidence, plus a bonus when both routes agree.
    conf_out = min(1.0, wsum / 2.0)
    if len(routes) == 2:
        za, zb = routes[0][0], routes[1][0]
        agree = 1.0 - min(1.0, abs(za - zb) / max(za, zb))
        conf_out = min(1.0, conf_out * (0.6 + 0.4 * agree) + 0.15 * agree)
    return round(float(z), 2), round(float(gap), 2), round(float(conf_out), 2)


def rolling_median(vals, win):
    n = len(vals)
    if n == 0:
        return vals
    half = win // 2
    out = np.empty(n)
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        out[i] = np.median(vals[lo:hi])
    return out


def temporal_for_track(frames_i, z_series, area_series, dt_frame):
    """Given a track's samples (processed-frame indices, Z, box area) compute the
    per-track temporal summary: min gap already handled by caller; here min TTC via
    both the metric slope and the scale-invariant area-expansion channels."""
    if len(z_series) < SLOPE_WIN:
        return None, None, None  # too short to differentiate reliably

    fi = np.asarray(frames_i, dtype=np.float64)
    z = rolling_median(np.asarray(z_series, dtype=np.float64), SMOOTH_WIN)
    ln_area = np.log(np.clip(np.asarray(area_series, dtype=np.float64), 1e-9, None))

    half = SLOPE_WIN // 2
    min_ttc = None
    min_ttc_si = None
    ttc_frame = None
    for i in range(len(z)):
        lo, hi = max(0, i - half), min(len(z), i + half + 1)
        if hi - lo < 4:
            continue
        # Metric closing speed: -dZ/dt from a line fit over the window.
        slope_z = np.polyfit(fi[lo:hi], z[lo:hi], 1)[0]        # m / processed-frame
        v_close = -slope_z / dt_frame                          # m/s (positive = closing)
        if v_close > MIN_CLOSING_MPS:
            ttc = z[i] / v_close
            if ttc > 0 and (min_ttc is None or ttc < min_ttc):
                min_ttc = ttc
                ttc_frame = int(fi[i])
        # Scale-invariant channel: TTC = 2 / d/dt(ln area) while the box grows.
        slope_a = np.polyfit(fi[lo:hi], ln_area[lo:hi], 1)[0] / dt_frame  # 1/s
        if slope_a > 1e-4:
            ttc_si = 2.0 / slope_a
            if min_ttc_si is None or ttc_si < min_ttc_si:
                min_ttc_si = ttc_si

    return (
        round(float(min_ttc), 2) if min_ttc is not None else None,
        round(float(min_ttc_si), 2) if min_ttc_si is not None else None,
        ttc_frame,
    )


def write_manifest():
    stems = sorted(p.name[: -len(".distances.json")] for p in DIST_DIR.glob("*.distances.json"))
    (DIST_DIR / "manifest.json").write_text(
        json.dumps({"videos": stems}, indent=2), encoding="utf-8"
    )
    return stems


def process(tracks_path, calib, force=False):
    stem = tracks_path.name[: -len(".tracks.json")]
    out_path = DIST_DIR / f"{stem}.distances.json"
    tmp_path = DIST_DIR / f"{stem}.distances.part.json"
    if out_path.exists() and not force:
        print(f"skip (already measured): {stem}", flush=True)
        return

    tr = json.loads(tracks_path.read_text(encoding="utf-8"))
    classes = tr.get("classes", {})
    fps = tr.get("fps") or 30.0
    stride = tr.get("stride", 1)
    dt_frame = stride / fps

    frames_in = tr["frames"]
    out_frames = []
    # Accumulate per-track series for the temporal pass.
    series = {}  # id -> {"fi":[], "z":[], "area":[], "cls":int}

    for fi, boxes in enumerate(frames_in):
        out_boxes = []
        for tid, cls, conf, x1, y1, x2, y2 in boxes:
            cls_name = classes.get(str(cls), str(cls))
            est = estimate_box(cls_name, conf, x1, y1, x2, y2, calib)
            if est is None:
                continue
            z_m, gap_m, c = est
            out_boxes.append([tid, cls, z_m, gap_m, c])
            s = series.setdefault(tid, {"fi": [], "z": [], "area": [], "cls": cls})
            s["fi"].append(fi)
            s["z"].append(z_m)
            s["area"].append(max(1e-6, (x2 - x1) * (y2 - y1)))
        out_frames.append(out_boxes)

    # Per-track summaries: closest approach + TTC (metric and scale-invariant).
    summary = {}
    for tid, s in series.items():
        if not s["z"]:
            continue
        gaps = [z - calib["bumper_offset_m"] for z in s["z"]]
        min_ttc, min_ttc_si, ttc_frame = temporal_for_track(
            s["fi"], s["z"], s["area"], dt_frame
        )
        summary[str(tid)] = {
            "cls": classes.get(str(s["cls"]), str(s["cls"])),
            "first": s["fi"][0],
            "last": s["fi"][-1],
            "count": len(s["fi"]),
            "min_gap_m": round(float(min(gaps)), 2),
            "min_ttc_s": min_ttc,
            "min_ttc_si_s": min_ttc_si,
            "ttc_frame": ttc_frame,
        }

    payload = {
        "video": tr.get("video"),
        "source": tracks_path.name,
        "fps": fps,
        "stride": stride,
        "frames_processed": len(out_frames),
        "classes": classes,
        "calibration": {
            "f_px": calib["f_px"],
            "v0_norm": calib["v0_norm"],
            "cam_h_m": calib["cam_h_m"],
            "bumper_offset_m": calib["bumper_offset_m"],
            "calibrated": calib.get("calibrated", False),
        },
        "note": ("distances are approximate — calibration is uncalibrated (estimated f_px, "
                 "v0). gap_m = distance from front bumper to object. TTC in seconds; "
                 "min_ttc_si_s is the calibration-free cross-check."),
        # frames[i] = [ [track_id, cls, Z_m, gap_m, conf], ... ] for the i-th processed frame.
        "frames": out_frames,
        "tracks": {k: summary[k] for k in sorted(summary, key=int)},
    }
    tmp_path.write_text(json.dumps(payload), encoding="utf-8")
    tmp_path.replace(out_path)

    n_read = sum(len(f) for f in out_frames)
    print(f"Done: {n_read} object-readings, {len(summary)} tracks -> {out_path.name}",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tracks", nargs="*", help="tracks/<stem>.tracks.json path(s)")
    ap.add_argument("--all", action="store_true", help="process every tracks JSON")
    ap.add_argument("--force", action="store_true", help="re-run even if output exists")
    args = ap.parse_args()

    if not CALIB_PATH.exists():
        sys.exit(f"missing calibration slot: {CALIB_PATH}")
    calib = load_calib()

    if args.all:
        files = sorted(TRACKS_DIR.glob("*.tracks.json"))
    else:
        if not args.tracks:
            sys.exit("give one or more tracks JSON paths, or --all")
        files = [Path(p) for p in args.tracks]
        missing = [f for f in files if not f.exists()]
        if missing:
            sys.exit("not found: " + ", ".join(str(m) for m in missing))

    if not files:
        sys.exit("no tracks JSON found in tracks/ — run make_tracks.py first")

    DIST_DIR.mkdir(exist_ok=True)
    if not calib.get("calibrated", False):
        print("NOTE: calibration is ESTIMATED (calibrated=false) — distances are "
              "approximate. Run the benchmark and update dashcam_calibration.json.", flush=True)
    for f in files:
        process(f, calib, force=args.force)
    stems = write_manifest()
    print(f"\n{len(stems)} clip(s) have distances.", flush=True)


if __name__ == "__main__":
    main()
