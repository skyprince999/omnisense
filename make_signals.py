"""Assign each video clip a driving-quality signal and write driving_signals.json.

Currently the signal is RANDOM (placeholder until real scoring exists in Phase 2/3):
    red   = bad driving
    amber = okay driving
    green = good driving

Clips are taken from detections/manifest.json (the same list the trip viewer
shows). Re-running keeps existing assignments for known clips and only rolls
signals for new ones, so the dots don't reshuffle on every run; use --reroll
to randomize everything afresh.

Usage:
    python make_signals.py            # assign signals to new clips, keep existing
    python make_signals.py --reroll   # re-randomize every clip
"""

import argparse
import json
import random
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
DETECT_MANIFEST = BASE_DIR / "detections" / "manifest.json"
OUT_PATH = BASE_DIR / "driving_signals.json"

SIGNALS = ["red", "amber", "green"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reroll", action="store_true", help="re-randomize every clip")
    args = ap.parse_args()

    stems = json.loads(DETECT_MANIFEST.read_text(encoding="utf-8"))["videos"]

    existing = {}
    if OUT_PATH.exists() and not args.reroll:
        existing = json.loads(OUT_PATH.read_text(encoding="utf-8")).get("signals", {})

    signals = {}
    rolled = 0
    for stem in stems:
        if stem in existing:
            signals[stem] = existing[stem]
        else:
            signals[stem] = random.choice(SIGNALS)
            rolled += 1

    payload = {
        "generated": date.today().isoformat(),
        "note": "random placeholder signals: red=bad, amber=okay, green=good driving",
        "signals": signals,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    counts = {s: sum(1 for v in signals.values() if v == s) for s in SIGNALS}
    print(f"{len(signals)} clips -> {OUT_PATH.name} "
          f"({rolled} newly rolled): {counts['green']} green, "
          f"{counts['amber']} amber, {counts['red']} red")


if __name__ == "__main__":
    main()
