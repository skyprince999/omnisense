"""Per-segment driving analysis over ALL videos via Sandbox Compute + understand (v5).

WHY v5 differs from v2-v4: those chained scene.describe() calls (P1->R1,
P2+R1->R2, P3+R1+R2->R3) on the hosted LLM tiers. Those tiers hit the Hackathon
dollar-budget lock, and the sandbox describe() path is broken server-side
(doubled frame URL 404 — see SANDBOX_BUG_REPORT.md). The WORKING route onto
Sandbox Compute is video.understand(), verified good on medium/Qwen3.5-27B.

But understand() is a BATCH, whole-video, single-pass API — it applies one
analyzer prompt across all time segments and cannot feed one segment's answer
into the next prompt. So the three chained stages are collapsed into ONE VLM
analyzer with a structured schema that returns, per 20s segment:
  - road_type / locality / weather / lighting   (was P1)
  - driving_signal red|amber|green + driving_review  (was P2)
  - suggestions                                  (was P3)

The model still reasons conditions -> review -> suggestions within one response.

Cost model: Sandbox is billed by wall-clock runtime (medium $3.50/hr), NOT per
request. So ONE sandbox is created for the whole corpus run and reused across
every video, then stopped in a finally. Total cost ~= run wall-time x $3.50.

Output per video: slices/<video name>.slices.v5.json  (own schema; does not
collide with the v2/v3/v4 files). A video whose v5 file already exists is
skipped without any API calls (the folder pre-check you asked for in v4).

Usage:
    python videodb_slices_v5.py                 # all un-analyzed videos, medium sandbox
    python videodb_slices_v5.py --only "Nagar"  # subset
    python videodb_slices_v5.py --video "1342"  # single video (validate output shape cheaply)
    python videodb_slices_v5.py --tier small    # Qwen3.5-9B (cheaper, lower quality)
    python videodb_slices_v5.py --yes           # skip the confirm prompt
    python videodb_slices_v5.py --list-stop     # emergency: stop every active sandbox

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
SLICES_DIR = BASE_DIR / "slices"

TIER_MODEL = {"small": "Qwen/Qwen3.5-9B", "medium": "Qwen/Qwen3.5-27B"}
TIER_RATE = {"small": 1.0, "medium": 3.5}

# One VLM analyzer replaces the P1/P2/P3 chain. The prompt walks the model through
# the same three stages; the schema makes each piece a separate, parseable field.
ANALYZER_PROMPT = (
    "You are analyzing a dashcam clip segment from a car driving in India. "
    "Work through three stages and fill every field.\n"
    "1) Conditions: road_type (village_road/city_road/highway), locality "
    "(rural/urban), weather (rain/summer/overcast), lighting (day/night/lowlight).\n"
    "2) Driving review: watch how the car is driven across the segment for "
    "tailgating, harsh/late braking, close passes to pedestrians/cyclists/animals, "
    "slow reaction to cut-ins, running lights, weaving/lane drift, risky overtakes. "
    "Set driving_signal to 'red' (dangerous), 'amber' (risky) or 'green' (safe), "
    "and give a one-to-two sentence driving_review justifying it.\n"
    "3) Coaching: 2-3 specific, actionable suggestions grounded in what is visible "
    "in this segment (following distance, speed for conditions, positioning, hazard "
    "anticipation). If the driving was safe, acknowledge it and give at most one "
    "refinement. Base everything only on visible evidence."
)

ANALYZER_SCHEMA = {
    "road_type": "string",
    "locality": "string",
    "weather": "string",
    "lighting": "string",
    "driving_signal": "string",
    "driving_review": "string",
    "suggestions": "string",
}

# Rough estimate for the confirm prompt: sandbox wall-time per video. Small clips
# ~2 min, longer parts scale with length; this is only a ballpark for the warning.
EST_MIN_PER_VIDEO = 2.5


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    key = os.environ.get("VIDEODB_API_KEY")
    if key:
        os.environ.setdefault("VIDEO_DB_API_KEY", key)  # SDK also reads the underscore form
    return key


def fmt(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def out_path_for(video):
    return SLICES_DIR / f"{video.name}.slices.v5.json"


def already_analyzed(video):
    """True if a non-empty v5 analysis file exists for this video (no API calls)."""
    p = out_path_for(video)
    if not p.exists():
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return bool(data.get("slices"))
    except (json.JSONDecodeError, ValueError):
        return False


def save(out_path, payload):
    tmp = out_path.with_suffix(".part.json")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(out_path)


def stop_sandbox(sandbox):
    try:
        print(f"Stopping sandbox {sandbox.id} ...")
        sandbox.stop()
        try:
            sandbox.wait_for_stop(timeout=120, interval=5)
        except Exception:
            pass
        print(f"  stopped (status: {getattr(sandbox, 'status', '?')})")
    except Exception as e:
        print(f"  !! FAILED to stop {getattr(sandbox, 'id', '?')}: {str(e)[:150]}")
        print("  !! Run --list-stop to ensure it is not left billing.")


def list_stop_all(conn):
    try:
        boxes = conn.list_sandboxes()
    except Exception as e:
        sys.exit(f"Could not list sandboxes: {str(e)[:200]}")
    active = [b for b in boxes if getattr(b, "is_active", False)
              or str(getattr(b, "status", "")).lower() in ("active", "ready", "running")]
    if not active:
        print("No active sandboxes.")
        return
    for b in active:
        print(f"Active: {b.id}  tier={getattr(b,'tier','?')}  status={getattr(b,'status','?')}")
        stop_sandbox(b)


# The VLM ignores the `schema` and returns prose, but it reliably emits each
# field as "field_name: value" (sometimes markdown-bolded). Pull them back out.
CATEGORICAL = ("road_type", "locality", "weather", "lighting", "driving_signal")


def _extract_field(text, field):
    """Find 'field: value' in the prose (tolerating **bold**, '-', '*' bullets)."""
    m = re.search(rf"{field}\s*[:\-]\s*\*{{0,2}}\s*([^\n*]+)", text, re.IGNORECASE)
    if not m:
        return None
    val = m.group(1).strip().strip("*").strip()
    return val or None


def _extract_signal(text):
    """driving_signal red|amber|green, near the label or anywhere as a fallback."""
    val = _extract_field(text, "driving_signal")
    if val:
        m = re.search(r"red|amber|green", val, re.IGNORECASE)
        if m:
            return m.group(0).lower()
    m = re.search(r"\b(red|amber|green)\b", text, re.IGNORECASE)
    return m.group(1).lower() if m else None


def normalize_segments(output, video_length, slice_seconds):
    """Coerce understand() output into [{start, end, <fields>, analysis}].

    Reality (see the raw_output): the analyzer returns {"scenes": [{"scene_id",
    "data": {"text"}, "start", "end"}...]} where start/end are null and text is
    prose. We regex the schema fields out of the prose, and — since the API drops
    per-scene times — derive approximate even-split timestamps from the video
    length and scene count (flagged approx_time).
    """
    scenes = None
    if isinstance(output, dict):
        for key in ("scenes", "segments", "results", "data"):
            if isinstance(output.get(key), list):
                scenes = output[key]
                break
    elif isinstance(output, list):
        scenes = output
    if not scenes:
        return []

    n = len(scenes)
    seg = (video_length / n) if (video_length and n) else slice_seconds
    records = []
    for i, s in enumerate(scenes):
        text = ""
        start = end = None
        if isinstance(s, dict):
            start = s.get("start", s.get("start_time"))
            end = s.get("end", s.get("end_time"))
            data = s.get("data") if isinstance(s.get("data"), dict) else s
            text = data.get("text") or data.get("description") or ""
            if not text and isinstance(s.get("text"), str):
                text = s["text"]
        else:
            text = str(s)

        approx = start is None
        if approx:
            start = round(i * seg, 1)
            end = round(min((i + 1) * seg, video_length or (i + 1) * seg), 1)

        rec = {"start": start, "end": end}
        if approx:
            rec["approx_time"] = True
        for f in ("road_type", "locality", "weather", "lighting"):
            v = _extract_field(text, f)
            if v:
                # Keep just the label, dropping any "(explanation)" or trailing clause.
                rec[f] = re.split(r"[(,.]", v)[0].strip()
        sig = _extract_signal(text)
        if sig:
            rec["driving_signal"] = sig
        rec["analysis"] = text.strip()
        records.append(rec)
    return records


def overall_signal(slices):
    """Worst signal across segments (red > amber > green), for a per-video dot."""
    order = {"red": 3, "amber": 2, "green": 1}
    sigs = [s.get("driving_signal") for s in slices if s.get("driving_signal") in order]
    return max(sigs, key=lambda x: order[x]) if sigs else None


def process_video(video, args, conn, sandbox_id, model):
    """Run one understand() pass over the video, routed to the sandbox. Store results."""
    from videodb.exceptions import VideodbError

    out_path = out_path_for(video)
    payload = {
        "video": video.name,
        "video_id": video.id,
        "slice_seconds": args.slice,
        "frames_per_segment": args.frames,
        "model": model,
        "sandbox_tier": args.tier,
        "prompt": ANALYZER_PROMPT,
        "schema": ANALYZER_SCHEMA,
        "generated": date.today().isoformat(),
        "slices": [],
    }
    try:
        understanding = video.understand(
            segmentation={"type": "time", "seconds": args.slice},
            analyzers=[{
                "type": "vlm",
                "name": "driving",
                "sampling": {"strategy": "uniform", "frame_count": args.frames},
                "config": {
                    "model": model,
                    "sandbox_id": sandbox_id,
                    "prompt": ANALYZER_PROMPT,
                    "schema": ANALYZER_SCHEMA,
                },
            }],
        )
        print(f"    run {understanding.id} — waiting...")
        understanding.wait_until_complete(timeout=args.timeout, poll_interval=10)
        analyzer = understanding.get_analyzer("driving")
        if not analyzer.is_successful:
            print(f"    analyzer status: {analyzer.status} (not successful)")
            payload["error"] = f"analyzer status {analyzer.status}"
            save(out_path, payload)
            return 0
        output = analyzer.get_output()
        payload["raw_output"] = output           # keep the exact server output too
        payload["slices"] = normalize_segments(
            output, getattr(video, "length", 0) or 0, args.slice)
        payload["overall_signal"] = overall_signal(payload["slices"])
        save(out_path, payload)
        n = len(payload["slices"])
        sig = [s.get("driving_signal") or "?" for s in payload["slices"]]
        print(f"    ok — {n} segment(s), signals: {', '.join(sig)} "
              f"(overall: {payload['overall_signal']}) -> {out_path.name}")
        return n
    except VideodbError as e:
        print(f"    UNDERSTAND ERROR: {str(e)[:200]}")
        payload["error"] = str(e)[:400]
        save(out_path, payload)
        return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="only videos whose name contains this substring")
    ap.add_argument("--video", help="single video (substring); overrides --only")
    ap.add_argument("--tier", choices=["small", "medium"], default="medium",
                    help="sandbox tier / model (default medium = Qwen3.5-27B)")
    ap.add_argument("--slice", type=int, default=20,
                    help="segment length in seconds (default 20)")
    ap.add_argument("--frames", type=int, default=3,
                    help="frames sampled per segment (default 3, for motion)")
    ap.add_argument("--timeout", type=int, default=1800,
                    help="seconds to wait for sandbox ready / each run (default 1800)")
    ap.add_argument("--force", action="store_true",
                    help="reprocess videos even if a v5 analysis file exists")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    ap.add_argument("--list-stop", action="store_true",
                    help="stop every active sandbox and exit (emergency cleanup)")
    args = ap.parse_args()

    if not load_env():
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")

    from videodb import connect, SandboxTier

    print("Connecting to VideoDB...")
    conn = connect(api_key=os.environ["VIDEODB_API_KEY"])

    if args.list_stop:
        list_stop_all(conn)
        return

    coll = conn.get_collection()
    videos = coll.get_videos()
    if args.video:
        needle = args.video.lower()
        videos = [v for v in videos if needle in (v.name or "").lower()]
    elif args.only:
        needle = args.only.lower()
        videos = [v for v in videos if needle in (v.name or "").lower()]
    if not videos:
        sys.exit("No videos match." if (args.video or args.only) else "No videos.")
    videos.sort(key=lambda v: getattr(v, "length", 0) or 0)  # smallest first

    SLICES_DIR.mkdir(exist_ok=True)

    # Folder pre-check: drop videos already analyzed (zero API calls).
    todo, already = [], []
    for v in videos:
        (already if (already_analyzed(v) and not args.force) else todo).append(v)

    model = TIER_MODEL[args.tier]
    rate = TIER_RATE[args.tier]
    print(f"\n{len(videos)} video(s): {len(already)} already analyzed, {len(todo)} to process")
    for v in already:
        print(f"  = {v.name}")
    for v in todo:
        print(f"  + {v.name}  ({fmt(getattr(v, 'length', 0) or 0)})")
    if not todo:
        print("\nNothing to do — every video already has a v5 analysis.")
        return

    est_min = len(todo) * EST_MIN_PER_VIDEO
    print(f"\nWill run on a {args.tier} sandbox ({model}, ${rate}/hr). "
          f"Rough wall-time ~{est_min:.0f} min -> ~${est_min/60*rate:.2f} "
          f"(+ provisioning). Sandbox is stopped at the end.")
    if not args.yes:
        try:
            if input("Proceed? [y/N]: ").strip().lower() not in ("y", "yes"):
                print("Aborted — nothing spent.")
                return
        except EOFError:
            print("Aborted (no TTY). Re-run with --yes.")
            return

    sandbox = None
    t0 = time.time()
    usage0 = conn.check_usage() or {}
    processed = failed = 0
    try:
        print(f"\nCreating {args.tier} sandbox ({model})...")
        sandbox = conn.create_sandbox(tier=getattr(SandboxTier, args.tier),
                                      models=[model], name="dashcam-v5")
        print(f"  sandbox {sandbox.id} — waiting up to {args.timeout}s...")
        sandbox.wait_for_ready(timeout=args.timeout, interval=5)
        print(f"  ready ({time.time()-t0:.0f}s). Processing {len(todo)} video(s).\n")

        for vi, video in enumerate(todo, 1):
            print(f"[{vi}/{len(todo)}] {video.name}  ({fmt(getattr(video,'length',0) or 0)})")
            try:
                n = process_video(video, args, conn, sandbox.id, model)
                processed += 1 if n else 0
                failed += 0 if n else 1
            except Exception as e:
                print(f"    VIDEO FAILED: {str(e)[:150]}")
                failed += 1
    except KeyboardInterrupt:
        print("\nInterrupted — stopping sandbox.")
    except Exception as e:
        print(f"\nRUN ERROR: {type(e).__name__}: {str(e)[:200]}")
    finally:
        if sandbox is not None:
            stop_sandbox(sandbox)

    usage1 = conn.check_usage() or {}
    d_used = (usage1.get("credit_used") or 0) - (usage0.get("credit_used") or 0)
    print(f"\n=== v5 run complete ===")
    print(f"videos ok: {processed}, failed: {failed}, already-analyzed (skipped): {len(already)}")
    print(f"wall time: {time.time()-t0:.0f}s   credits spent: {d_used:.4f}   "
          f"balance now: {usage1.get('credit_balance')}")


if __name__ == "__main__":
    main()
