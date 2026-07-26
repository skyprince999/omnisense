"""Send a custom vision prompt to a specific VideoDB video.

Unlike videodb_query.py (which semantically SEARCHES an existing scene index),
this script RUNS A PROMPT against the video: it creates a new scene index whose
per-scene "descriptions" are the vision model's answers to your prompt, one per
time window (default 25 s). Great for structured/classification prompts that
ask for JSON — each window gets its own JSON answer, and if the answers parse
as JSON the script also prints a majority-vote summary across windows.

Flow:
  1. Pick the video — via --video <name substring> or an interactive menu.
  2. Provide the prompt — via --prompt, --prompt-file, or interactive paste
     (finish with a line containing only END).
  3. The script indexes the video with that prompt, waits, then prints every
     scene window's answer.

Notes:
  - Each distinct prompt creates (and bills) a new scene index the first time;
    re-running with the same prompt reuses the server's existing copy.
  - VideoDB's status API often reports 'failed' for indexes that ingested fine
    (see PHASE1_SEARCH_PLAN.md). get_scene_index() refuses to read those, so
    the script falls back to pulling answers out via search on that index.

Usage:
    python videodb_prompt.py --video "part 3 of 9" --prompt-file prompt_road_conditions.txt
    python videodb_prompt.py --video "Car Dashcam" --prompt "Is the road wet or dry? Answer in one word."
    python videodb_prompt.py                       # fully interactive
    python videodb_prompt.py ... --time 60         # one answer per 60 s instead of 25 s

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent

DONE_STATUSES = {"done", "completed", "success"}
FAILED_STATUSES = {"failed", "error"}
POLL_SECS = 10
TIMEOUT_SECS = 20 * 60


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def fmt(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def pick_video(videos):
    print(f"\n{len(videos)} videos in the collection:\n")
    for i, v in enumerate(videos, 1):
        print(f"  [{i:2d}] {v.name}   ({fmt(getattr(v, 'length', 0) or 0)})")
    while True:
        choice = input("\nSelect a video number (or q to quit): ").strip().lower()
        if choice in ("q", "quit", "exit"):
            return None
        try:
            n = int(choice)
            if 1 <= n <= len(videos):
                return videos[n - 1]
        except ValueError:
            pass
        print(f"  enter a number between 1 and {len(videos)}")


def resolve_video(videos, needle):
    """--video substring -> exactly one video, or explain and exit."""
    matches = [v for v in videos if needle.lower() in (v.name or "").lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        sys.exit(f"No video name contains {needle!r}. Run without --video to see the menu.")
    print(f"--video {needle!r} matches {len(matches)} videos:")
    for v in matches:
        print(f"  - {v.name}")
    sys.exit("Refine the substring so it matches exactly one.")


def read_prompt(args):
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    print("\nPaste your prompt. Finish with a line containing only END "
          "(or Ctrl+Z then Enter on Windows):\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    prompt = "\n".join(lines).strip()
    if not prompt:
        sys.exit("Empty prompt.")
    return prompt


def index_status(video, idx_id):
    try:
        for idx in video.list_scene_index():
            if idx.get("scene_index_id") == idx_id:
                return idx.get("status")
    except Exception:
        pass
    return None


def run_prompt(video, prompt, args, SceneExtractionType, InvalidRequestError):
    """Create (or reuse) a scene index for this prompt; return its id."""
    tier = args.model or "ultra (server default)"
    print(f"\nRunning prompt over {video.name!r} "
          f"(one answer per {args.time}s window, model tier: {tier})...")
    try:
        idx_id = video.index_scenes(
            extraction_type=SceneExtractionType.time_based,
            extraction_config={"time": args.time, "select_frames": ["first"]},
            prompt=prompt,
            model_name=args.model,
            name=f"custom-prompt {video.name}"[:80],
        )
    except InvalidRequestError as e:
        # Same prompt was run before — the server keeps one copy per
        # (llm_tier, prompt) and its duplicate check is authoritative.
        m = re.search(r"index with id (\w+) already exists", str(e))
        if m:
            print(f"  this prompt was already run on this video — reusing index {m.group(1)}")
            return m.group(1)
        sys.exit(f"index request failed: {str(e)[:300]}")

    waited = 0
    last = None
    while waited < TIMEOUT_SECS:
        s = index_status(video, idx_id)
        if s != last:
            print(f"  status: {s}")
            last = s
        if s in DONE_STATUSES or s in FAILED_STATUSES:
            break
        time.sleep(POLL_SECS)
        waited += POLL_SECS
    if last in FAILED_STATUSES:
        print("  (status says 'failed' — usually bogus; trying to read the answers anyway)")
    return idx_id


def fetch_answers(video, idx_id, prompt, expected, IndexType, InvalidRequestError):
    """Return [(start, end, text)] for every scene window of the index."""
    # Preferred path: read the records directly (works when status is 'done').
    try:
        recs = video.get_scene_index(idx_id)
        return [(r.get("start"), r.get("end"), r.get("description") or "") for r in recs]
    except Exception:
        pass
    # Fallback for 'failed'-status indexes (see PHASE1_SEARCH_PLAN.md): the
    # answers ARE in the search corpus, but (a) the index_id search param is not
    # honored server-side — shots must be filtered client-side by their
    # scene_index_id — and (b) each query returns only the top ~15 shots, so we
    # fire several differently-worded queries (the prompt's own vocabulary ranks
    # its answers highest) and merge until all expected windows are recovered.
    queries = [
        " ".join(prompt.split())[:200],
        "road traffic vehicles weather lighting scene",
        "street highway rural urban day night",
    ]
    found = {}  # rounded start -> (start, end, text)
    for q in queries:
        try:
            res = video.search(q, index_type=IndexType.scene, result_threshold=200)
        except InvalidRequestError:
            continue
        for s in res.get_shots():
            if getattr(s, "scene_index_id", None) != idx_id:
                continue
            key = round(s.start or 0)
            if key not in found:
                found[key] = (s.start, s.end, getattr(s, "text", "") or "")
        if expected and len(found) >= expected:
            break
    if expected and len(found) < expected:
        print(f"  (recovered {len(found)}/{expected} windows via search fallback)")
    return [found[k] for k in sorted(found)]


def parse_json_answer(text):
    """Try to parse a scene answer as JSON (tolerating ```json fences)."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(t[start:end + 1])
    except json.JSONDecodeError:
        return None


def print_answers(answers):
    parsed = []
    for start, end, text in answers:
        print(f"\n--- {fmt(start)} - {fmt(end)} " + "-" * 50)
        j = parse_json_answer(text)
        if j is not None:
            parsed.append(j)
            print(json.dumps(j, indent=2))
        else:
            print(text.strip())

    # Majority vote across windows for flat label fields (e.g. road_type).
    # Free-text fields (like "notes") are skipped: short-valued keys only,
    # and only when at least two windows agree on something.
    if len(parsed) > 1:
        keys = [k for k in parsed[0]
                if isinstance(parsed[0][k], str) and len(parsed[0][k]) <= 30]
        summary = []
        for k in keys:
            votes = Counter(p.get(k, "") for p in parsed if isinstance(p.get(k), str))
            if votes and votes.most_common(1)[0][1] > 1:
                summary.append((k, votes))
        if summary:
            print("\n=== Majority across windows " + "=" * 40)
            for k, votes in summary:
                top, n = votes.most_common(1)[0]
                print(f"  {k}: {top}   ({n}/{len(parsed)} windows; "
                      + ", ".join(f"{v}={c}" for v, c in votes.most_common()) + ")")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("--video", help="video name substring (must match exactly one)")
    ap.add_argument("--prompt", help="the prompt text")
    ap.add_argument("--prompt-file", help="file containing the prompt")
    ap.add_argument("--time", type=int, default=25,
                    help="seconds per scene window / answer (default 25)")
    ap.add_argument("--model", choices=["basic", "pro", "ultra"],
                    help="LLM tier for inference (omitted = server default, "
                         "which is ultra — the most expensive). basic is ~5x "
                         "cheaper per llm unit; pro is in between. NOTE: the "
                         "tier is part of the index identity, so the same "
                         "prompt at a different tier creates a separate index.")
    args = ap.parse_args()

    load_env()
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")

    from videodb import connect, IndexType, SceneExtractionType
    from videodb.exceptions import InvalidRequestError

    print("Connecting to VideoDB...")
    conn = connect(api_key=api_key)
    coll = conn.get_collection()
    videos = sorted(coll.get_videos(), key=lambda v: v.name or "")
    if not videos:
        sys.exit("No videos in the collection.")

    video = resolve_video(videos, args.video) if args.video else pick_video(videos)
    if video is None:
        return
    prompt = read_prompt(args)

    idx_id = run_prompt(video, prompt, args, SceneExtractionType, InvalidRequestError)
    expected = -(-int(getattr(video, "length", 0) or 0) // args.time)  # ceil
    answers = fetch_answers(video, idx_id, prompt, expected, IndexType, InvalidRequestError)
    if not answers:
        sys.exit("Could not retrieve any answers for this index — try re-running; "
                 "if it persists the indexing genuinely failed.")
    print(f"\n{len(answers)} scene window(s) answered:")
    print_answers(answers)


if __name__ == "__main__":
    main()
