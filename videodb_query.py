"""Interactively query a single video indexed on VideoDB.

Flow:
  1. Lists every video in the collection as a numbered menu — pick one.
  2. Asks for a natural-language query (e.g. "pedestrian crossing the road").
  3. Runs semantic scene search on that video only and prints timestamped
     hits + a playable HLS stream URL compiled from the matching moments.

After each answer you can type another query for the same video, or:
  v  — pick a different video
  q  — quit

Usage:
    python videodb_query.py                # interactive (menu + prompt)
    python videodb_query.py --score 0.45   # stricter relevance threshold
    python videodb_query.py --limit 8      # more results per query

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

BASE_DIR = Path(__file__).parent


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
    """Numbered menu over the collection; returns the chosen Video or None."""
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


def run_query(video, query, args, IndexType, InvalidRequestError):
    try:
        res = video.search(
            query,
            index_type=IndexType.scene,
            score_threshold=args.score,
            result_threshold=args.limit,
        )
    except InvalidRequestError as e:
        # Empty result sets raise instead of returning [] — treat as "no matches".
        if "no results" in str(e).lower():
            print("  no matches")
        else:
            print(f"  search failed: {str(e)[:200]}")
        return
    except Exception as e:
        print(f"  search error: {str(e)[:200]}")
        return

    shots = res.get_shots()
    if not shots:
        print("  no matches")
        return
    for shot in shots:
        text = " ".join((getattr(shot, "text", "") or "").split())
        print(f"  {fmt(shot.start)}-{fmt(shot.end)}  "
              f"score={round(getattr(shot, 'search_score', 0) or 0, 2)}")
        print(textwrap.fill(text, width=100, initial_indent="      ",
                            subsequent_indent="      "))
    try:
        print(f"\n  clip reel of these moments: {res.compile()}")
    except Exception as e:
        print(f"  (could not compile stream: {str(e)[:120]})")


def main():
    # Scene descriptions contain unicode punctuation; avoid cp1252 mojibake.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("--score", type=float, default=0.2,
                    help="score threshold (default 0.2; try 0.45 for strict matches)")
    ap.add_argument("--limit", type=int, default=5,
                    help="max results per query (default 5)")
    args = ap.parse_args()

    load_env()
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")

    from videodb import connect, IndexType
    from videodb.exceptions import InvalidRequestError

    print("Connecting to VideoDB...")
    conn = connect(api_key=api_key)
    coll = conn.get_collection()
    videos = sorted(coll.get_videos(), key=lambda v: v.name or "")
    if not videos:
        sys.exit("No videos in the collection.")

    video = pick_video(videos)
    while video is not None:
        print(f"\nQuerying: {video.name}")
        print("Type a query, or  v = switch video,  q = quit")
        while True:
            try:
                query = input("\nquery> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not query:
                continue
            if query.lower() in ("q", "quit", "exit"):
                return
            if query.lower() == "v":
                video = pick_video(videos)
                break
            run_query(video, query, args, IndexType, InvalidRequestError)


if __name__ == "__main__":
    main()
