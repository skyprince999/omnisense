"""Measure VideoDB credit costs — overall, or of any operation you run.

VideoDB does not expose per-request cost or token counts anywhere (the describe/
index/search responses carry no usage metadata, and GET /billing/usage returns
only account-level cumulative counters). What it DOES return is every line
item's cumulative units plus a `cost_metric` rate table (credits per unit) —
so cost can be MEASURED by snapshotting the counters before an operation and
diffing after:

    python videodb_cost.py               # current balance + nonzero usage, costed
    python videodb_cost.py --mark        # save a snapshot (the "before" point)
    ... run any operation (a script, one query, an index) ...
    python videodb_cost.py --diff        # what changed since the mark, per line item
    python videodb_cost.py --diff --mark # diff, then re-mark (chained measurements)

The diff shows, per line item: units consumed, rate, and credits spent — plus
the total from the credit_used counter. Caveats: counters are account-wide (any
concurrent activity pollutes the diff) and can lag a little behind the request.

Requires VIDEODB_API_KEY in the environment or a .env file next to this script.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
SNAPSHOT_PATH = BASE_DIR / ".usage_snapshot.json"

# Response fields that aren't usage counters.
NON_COUNTERS = {"credit_balance", "credit_used", "cost_metric", "email", "name",
                "plan_id", "subscription_status", "user_id"}


def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def fetch_usage():
    load_env()
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        sys.exit("VIDEODB_API_KEY is not set (environment or .env).")
    from videodb import connect
    return connect(api_key=api_key).check_usage()


def counters(usage):
    return {k: v for k, v in usage.items()
            if k not in NON_COUNTERS and isinstance(v, (int, float))}


def cost_of(usage, item, units):
    rate = (usage.get("cost_metric") or {}).get(item, 0) or 0
    return units * rate


def print_current(usage):
    rates = usage.get("cost_metric") or {}
    print(f"Account: {usage.get('email')}   plan: {usage.get('plan_id')}")
    print(f"Credits: {usage.get('credit_balance'):.4f} left, "
          f"{usage.get('credit_used'):.4f} used\n")
    print(f"{'line item':28} {'units':>12} {'rate':>10} {'credits':>10}")
    rows = [(k, v, rates.get(k, 0) or 0) for k, v in sorted(counters(usage).items()) if v]
    for k, v, r in rows:
        print(f"{k:28} {v:>12.4f} {r:>10.5f} {v * r:>10.4f}")
    print(f"\n(estimated from units x rate; authoritative total is credit_used)")


def print_diff(before, after):
    when = before.get("_marked_at")
    if when:
        print(f"Changes since mark ({when}):\n")
    b, a = counters(before), counters(after)
    rates = after.get("cost_metric") or {}
    total_est = 0.0
    any_change = False
    print(f"{'line item':28} {'d-units':>12} {'rate':>10} {'credits':>10}")
    for k in sorted(set(b) | set(a)):
        d = (a.get(k) or 0) - (b.get(k) or 0)
        if abs(d) < 1e-9:
            continue
        any_change = True
        r = rates.get(k, 0) or 0
        total_est += d * r
        print(f"{k:28} {d:>12.4f} {r:>10.5f} {d * r:>10.4f}")
    if not any_change:
        print("  (no line-item changes recorded yet — counters can lag; retry shortly)")
    d_used = (after.get("credit_used") or 0) - (before.get("credit_used") or 0)
    print(f"\n{'estimated total':28} {'':>12} {'':>10} {total_est:>10.4f}")
    print(f"{'actual credits spent':28} {'':>12} {'':>10} {d_used:>10.4f}"
          f"   (credit_used delta — authoritative)")
    print(f"{'balance now':28} {'':>12} {'':>10} {after.get('credit_balance'):>10.4f}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", action="store_true",
                    help="save the current counters as the measurement baseline")
    ap.add_argument("--diff", action="store_true",
                    help="show per-line-item cost since the last --mark")
    args = ap.parse_args()

    usage = fetch_usage()

    if args.diff:
        if not SNAPSHOT_PATH.exists():
            sys.exit("No snapshot found — run with --mark first.")
        before = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        print_diff(before, usage)
    elif not args.mark:
        print_current(usage)

    if args.mark:
        usage["_marked_at"] = datetime.now().isoformat(timespec="seconds")
        SNAPSHOT_PATH.write_text(json.dumps(usage), encoding="utf-8")
        print(("\n" if args.diff else "") + f"Marked baseline at {usage['_marked_at']}.")


if __name__ == "__main__":
    main()
