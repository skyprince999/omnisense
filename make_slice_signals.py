"""Compute each clip's driving-quality dot from its slices and write driving_signals.json.

Replaces the old random placeholder in make_signals.py with a real rule that reads
through every clip's slices manifest (slices/<stem>.slices.v5.json) and aggregates the
per-slice driving_signal into one clip-level signal:

    red    if the clip has ANY red slice
    amber  else if amber slices are > AMBER_FRAC (10%) of the clip's slices
    green  otherwise (the default)

This is the manifest the trip viewers read (loadSignals -> driving_signals.json) to
colour the dot next to each clip in the Segments sidebar.

Usage:
    python make_slice_signals.py                 # -> driving_signals.json
    python make_slice_signals.py --version v2    # aggregate *.slices.v2.json instead
    python make_slice_signals.py --amber-frac 0.15
"""
import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
DETECT_MANIFEST = BASE_DIR / "detections" / "manifest.json"
SLICES_DIR = BASE_DIR / "slices"
OUT_PATH = BASE_DIR / "driving_signals.json"

AMBER_FRAC_DEFAULT = 0.10


def aggregate(slices, amber_frac):
    """Roll a clip's per-slice signals into one clip-level signal, with the counts."""
    counts = Counter((s.get("driving_signal") or "green").lower() for s in slices)
    total = len(slices)
    red = counts.get("red", 0)
    amber = counts.get("amber", 0)
    if total == 0:
        signal = None
    elif red > 0:
        signal = "red"
    elif amber / total > amber_frac:
        signal = "amber"
    else:
        signal = "green"
    return signal, {
        "total": total,
        "green": counts.get("green", 0),
        "amber": amber,
        "red": red,
        "amber_pct": round(amber / total * 100, 1) if total else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v5", help="slices file version (v5 or v2)")
    ap.add_argument("--amber-frac", type=float, default=AMBER_FRAC_DEFAULT,
                    help="amber share of a clip's slices above which the dot is amber (default 0.10)")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    # clip list = the same one the viewers show
    stems = json.loads(DETECT_MANIFEST.read_text(encoding="utf-8"))["videos"]
    suffix = f".slices.{args.version}.json"

    signals, detail, missing = {}, {}, []
    for stem in stems:
        path = SLICES_DIR / (stem + suffix)
        if not path.exists():
            signals[stem] = None
            missing.append(stem)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        sig, counts = aggregate(data.get("slices", []) or [], args.amber_frac)
        signals[stem] = sig
        detail[stem] = counts

    payload = {
        "generated": date.today().isoformat(),
        "source": f"slices/*.slices.{args.version}.json",
        "rule": (f"red if any red slice; else amber if amber > "
                 f"{args.amber_frac:.0%} of the clip's slices; else green"),
        "amber_frac": args.amber_frac,
        "signals": signals,
        "detail": detail,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    c = Counter(v for v in signals.values() if v)
    print(f"{len(signals)} clips -> {Path(args.out).name}: "
          f"{c.get('green', 0)} green, {c.get('amber', 0)} amber, {c.get('red', 0)} red"
          + (f", {len(missing)} without slices" if missing else ""))
    for stem in missing:
        print(f"  ! no {suffix} for: {stem}")


if __name__ == "__main__":
    main()
