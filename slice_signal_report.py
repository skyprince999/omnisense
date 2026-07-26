"""Summarize driving-quality slices across all clips.

Reads every slices manifest in `slices/` (default: the v5 files, which carry a
`driving_signal` of green/amber/red per slice) and, for each video clip, counts how
many green / amber / red slices it has. Writes a markdown report.

Usage:
    python slice_signal_report.py                     # -> slice_signal_report.md
    python slice_signal_report.py --version v2        # use *.slices.v2.json instead
    python slice_signal_report.py --out report.md
"""
import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICES_DIR = HERE / "slices"

# maps each clip stem to a trip, mirroring the viewers' TRIPS prefixes
TRIPS = [
    ("Pimpri Underpass", "Car Dashcam"),
    ("Bhandardara Trip", "Good videos"),
    ("Nagar Highway", "Nagar highway trip"),
    ("Nigdi to Yerwada", "Nigdi to Yerwada"),
    ("Pune to Velhe", "Pune to Velhe"),
    ("VN to PIC Pashan", "VN to PIC Pashan"),
]
SIGNALS = ("green", "amber", "red")


def trip_for(stem):
    for name, prefix in TRIPS:
        if stem.startswith(prefix):
            return name
    return "Other"


def worst(counts):
    """The most severe signal actually present in the clip."""
    for sig in ("red", "amber", "green"):
        if counts.get(sig, 0) > 0:
            return sig
    return "—"


def collect(version):
    suffix = f".slices.{version}.json"
    rows = []
    for path in sorted(SLICES_DIR.glob(f"*{suffix}")):
        stem = path.name[: -len(suffix)]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! skip {path.name}: {e}")
            continue
        slices = data.get("slices", []) or []
        counts = Counter((s.get("driving_signal") or "unknown").lower() for s in slices)
        rows.append({
            "stem": stem,
            "trip": trip_for(stem),
            "total": len(slices),
            "green": counts.get("green", 0),
            "amber": counts.get("amber", 0),
            "red": counts.get("red", 0),
            "unknown": sum(v for k, v in counts.items() if k not in SIGNALS),
            "worst": worst(counts),
        })
    return rows


ICON = {"red": "🔴", "amber": "🟠", "green": "🟢", "—": "—"}


def write_md(rows, version, out_path):
    total = {k: sum(r[k] for r in rows) for k in ("total", "green", "amber", "red", "unknown")}
    any_unknown = total["unknown"] > 0

    lines = []
    lines.append("# Driving-slice signal report")
    lines.append("")
    lines.append(f"Source: `slices/*.slices.{version}.json` — {len(rows)} clips, "
                 f"{total['total']} slices total.")
    lines.append("")

    # overall summary
    lines.append("## Overall")
    lines.append("")
    lines.append("| Signal | Slices | Share |")
    lines.append("|---|--:|--:|")
    denom = total["total"] or 1
    for sig in SIGNALS:
        lines.append(f"| {ICON[sig]} {sig} | {total[sig]} | {total[sig] / denom:.0%} |")
    if any_unknown:
        lines.append(f"| ⚪ unknown | {total['unknown']} | {total['unknown'] / denom:.0%} |")
    lines.append("")

    # per-clip table, grouped by trip
    lines.append("## Per clip")
    lines.append("")
    header = "| Clip | Total | 🟢 green | 🟠 amber | 🔴 red |" + (" ⚪ ? |" if any_unknown else "") + " Worst |"
    divide = "|---|--:|--:|--:|--:|" + ("--:|" if any_unknown else "") + ":--:|"

    trip_order = [name for name, _ in TRIPS] + ["Other"]
    for trip in trip_order:
        trip_rows = [r for r in rows if r["trip"] == trip]
        if not trip_rows:
            continue
        lines.append(f"### {trip}")
        lines.append("")
        lines.append(header)
        lines.append(divide)
        for r in trip_rows:
            row = f"| {r['stem']} | {r['total']} | {r['green']} | {r['amber']} | {r['red']} |"
            if any_unknown:
                row += f" {r['unknown']} |"
            row += f" {ICON[r['worst']]} {r['worst']} |"
            lines.append(row)
        # trip subtotal
        sub = {k: sum(r[k] for r in trip_rows) for k in ("total", "green", "amber", "red", "unknown")}
        sub_row = f"| **{trip} subtotal** | **{sub['total']}** | **{sub['green']}** | **{sub['amber']}** | **{sub['red']}** |"
        if any_unknown:
            sub_row += f" **{sub['unknown']}** |"
        sub_row += " |"
        lines.append(sub_row)
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v5", help="slices file version (v5 or v2)")
    ap.add_argument("--out", default=str(HERE / "slice_signal_report.md"))
    args = ap.parse_args()

    rows = collect(args.version)
    if not rows:
        print(f"No slices/*.slices.{args.version}.json files found in {SLICES_DIR}")
        return
    total = write_md(rows, args.version, Path(args.out))
    print(f"{len(rows)} clips, {total['total']} slices  "
          f"(green {total['green']}, amber {total['amber']}, red {total['red']}"
          + (f", unknown {total['unknown']}" if total['unknown'] else "") + ")")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
