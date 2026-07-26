"""Normalize the coaching notes on risky slices into conversational voiceover lines.

For every slice whose driving_signal is amber or red, this pulls the coaching
instruction out of the slice's markdown `analysis` blob, sends it to OpenAI to be
rewritten as one or two natural spoken sentences (suitable for a TTS nudge), and
stores the result on a new `coaching` key on that slice. Green slices are left alone.

The key (from .env `OPENAI_KEY` / `OPENAI_API_KEY`, or --key) is required.
The run is idempotent/resumable: slices that already have a `coaching` string are
skipped unless --force, and each file is rewritten atomically after every call, so an
interrupted run never loses finished work or leaves a truncated file.

Usage:
    python make_slice_coaching.py --dry-run          # show what would be sent, no API calls
    python make_slice_coaching.py --limit 3          # do just the first 3 (smoke test)
    python make_slice_coaching.py                     # normalize every amber/red slice
    python make_slice_coaching.py --force             # redo even slices that already have it
    python make_slice_coaching.py --model gpt-4o
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICES_DIR = HERE / "slices"

TARGET_SIGNALS = {"amber", "red"}

SYSTEM_PROMPT = (
    "You are a warm, encouraging in-car driving coach. You are given terse coaching "
    "notes extracted from a dashcam review of a short clip. Rewrite them as one or two "
    "natural, conversational spoken sentences, addressed directly to the driver as "
    "\"you\". It will be read aloud as a brief voice nudge, so keep it concise (aim for "
    "under 35 words), specific, and actionable. Do not use markdown, bullet points, "
    "headings, or lists. Do not add greetings, names, or sign-offs. Return only the "
    "spoken line."
)


def load_key(cli_key):
    if cli_key:
        return cli_key
    for name in ("OPENAI_KEY", "OPENAI_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() in ("OPENAI_KEY", "OPENAI_API_KEY"):
                return v.strip().strip('"').strip("'")
    return None


def coaching_notes(analysis):
    """Pull the coaching section out of a slice's markdown 'analysis' blob."""
    if not analysis:
        return ""
    t = analysis
    m = re.search(r"3\)[\s*]*Coaching[^\n]*\n", analysis, re.I) or \
        re.search(r"Coaching[^\n]*\n", analysis, re.I)
    if m:
        t = analysis[m.end():]
    lines = [
        re.sub(r"[*#>_`]+", "", ln).lstrip("-• ").strip()
        for ln in t.splitlines()
    ]
    cleaned = "  ".join(x for x in lines if x)
    cleaned = re.sub(r"\s{2,}", "  ", cleaned).strip()
    if cleaned:
        return cleaned
    # fall back to the whole analysis, de-marked
    return re.sub(r"\s{2,}", " ", re.sub(r"[*#>_`]+", " ", analysis)).strip()


def normalize(client, model, notes):
    """One OpenAI call with a single retry on transient failure."""
    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": notes},
                ],
                temperature=0.4,
                max_tokens=120,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
                continue
            raise


def atomic_write(path, data):
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v5", help="slices file version (default v5)")
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--force", action="store_true", help="redo slices that already have coaching")
    ap.add_argument("--limit", type=int, default=0, help="process at most N slices (0 = all)")
    ap.add_argument("--dry-run", action="store_true", help="print extracted notes, make no API calls")
    ap.add_argument("--key", default=None)
    args = ap.parse_args()

    suffix = f".slices.{args.version}.json"
    files = sorted(SLICES_DIR.glob(f"*{suffix}"))
    if not files:
        sys.exit(f"No slices/*{suffix} files found.")

    # count targets up front
    targets = 0
    for f in files:
        for s in json.loads(f.read_text(encoding="utf-8")).get("slices", []):
            if (s.get("driving_signal") or "").lower() in TARGET_SIGNALS:
                if args.force or not (s.get("coaching") or "").strip():
                    targets += 1
    print(f"{len(files)} files, {targets} amber/red slices to normalize"
          + (" (dry run)" if args.dry_run else f" via {args.model}"))

    client = None
    if not args.dry_run:
        key = load_key(args.key)
        if not key:
            sys.exit("No OpenAI key. Add OPENAI_KEY=... to .env or pass --key.")
        from openai import OpenAI
        client = OpenAI(api_key=key)

    done = errors = 0
    stop = False
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for i, s in enumerate(data.get("slices", [])):
            if (s.get("driving_signal") or "").lower() not in TARGET_SIGNALS:
                continue
            if not args.force and (s.get("coaching") or "").strip():
                continue
            notes = coaching_notes(s.get("analysis", ""))
            if not notes:
                continue
            if args.dry_run:
                print(f"\n[{f.name} slice {i} {s.get('driving_signal')}]")
                print("  NOTES:", notes[:200])
                done += 1
            else:
                try:
                    line = normalize(client, args.model, notes)
                    s["coaching"] = line
                    changed = True
                    done += 1
                    print(f"[{done}/{targets}] {f.name[:38]} s{i}: {line[:90]}")
                    atomic_write(f, data)  # flush after each call for resumability
                except Exception as e:
                    errors += 1
                    print(f"  ! error on {f.name} slice {i}: {e}")
            if args.limit and done >= args.limit:
                stop = True
                break
        if changed and not args.dry_run:
            atomic_write(f, data)
        if stop:
            break

    print(f"\nDone: {done} slices normalized"
          + (f", {errors} errors" if errors else "")
          + (" (dry run — nothing written)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
