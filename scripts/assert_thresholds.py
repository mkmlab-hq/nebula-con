#!/usr/bin/env python
"""
Assert metric thresholds against profile.
Usage:
  python scripts/assert_thresholds.py --metrics metrics/axes_run.json --profile config/metrics_profile_default.json
Exit codes:
  0 = success
  1 = hard failure (threshold violation)
  2 = file / schema issue
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

def load_json(p: Path) -> Dict[str, Any]:
    if not p.exists():
        print(f"[ERROR] File not found: {p}", file=sys.stderr)
        sys.exit(2)
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse {p}: {e}", file=sys.stderr)
        sys.exit(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="metrics/axes_run.json")
    ap.add_argument("--profile", default="config/metrics_profile_default.json")
    ap.add_argument("--fail-on-warn", action="store_true", help="Upgrade warnings to failures")
    args = ap.parse_args()

    metrics = load_json(Path(args.metrics))
    profile = load_json(Path(args.profile))

    prof_metrics = profile.get("metrics", {})
    if not prof_metrics:
        print("[ERROR] Profile missing 'metrics' section", file=sys.stderr)
        sys.exit(2)

    fail = False
    warnings = 0

    for key, spec in prof_metrics.items():
        allow_none = spec.get("allow_none", False)
        severity = spec.get("severity", "error")
        min_v = spec.get("min", None)
        max_v = spec.get("max", None)
        warn_above = spec.get("warn_above", None)
        value = metrics.get(key, None)

        if value is None:
            if not allow_none:
                print(f"[ERROR] Metric '{key}' is None but allow_none=False")
                fail = True
            else:
                print(f"[INFO] Metric '{key}' is None (allowed)")
            continue

        # Type check
        if isinstance(value, (int, float)):
            num_val = float(value)
        else:
            print(f"[ERROR] Metric '{key}' is not numeric: {value}")
            fail = True
            continue

        if min_v is not None and num_val < min_v:
            print(f"[ERROR] Metric '{key}' value {num_val} < min {min_v}")
            fail = True
        if max_v is not None and num_val > max_v:
            print(f"[ERROR] Metric '{key}' value {num_val} > max {max_v}")
            fail = True

        if warn_above is not None and num_val > warn_above:
            msg = f"[WARN] Metric '{key}' value {num_val} > warn_above {warn_above}"
            if args.fail_on_warn:
                print(msg.replace("[WARN]", "[FAIL]"))
                fail = True
            else:
                print(msg)
                warnings += 1

    if fail:
        print("[RESULT] Threshold assertions FAILED", file=sys.stderr)
        sys.exit(1)

    print(f"[RESULT] Threshold assertions PASSED (warnings={warnings})")
    sys.exit(0)

if __name__ == "__main__":
    main() 