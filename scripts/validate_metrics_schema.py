#!/usr/bin/env python
"""
Validate metrics JSON using a pydantic schema.
Usage:
  python scripts/validate_metrics_schema.py --file metrics/axes_run.json
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, field_validator

class AxesMetrics(BaseModel):
    st_var_ratio: float
    seasonal_corr: float
    psi_trigger_rate: float
    sk_k_score: float
    outlier_impact: float
    dip_stat: Optional[float] = None
    intra_cluster_density: Optional[float] = None
    silhouette_approx: Optional[float] = None
    density_k: Optional[int] = None

    @field_validator(
        "st_var_ratio","seasonal_corr","psi_trigger_rate","sk_k_score","outlier_impact",
        "dip_stat","intra_cluster_density","silhouette_approx", mode="before"
    )
    def allow_none_or_numeric(cls, v):
        if v is None:
            return v
        if isinstance(v, (int, float)):
            return float(v)
        raise ValueError("Must be numeric or None")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="metrics/axes_run.json")
    args = ap.parse_args()

    p = Path(args.file)
    if not p.exists():
        print(f"[ERROR] Metrics file not found: {p}", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] JSON parse failed: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        AxesMetrics(**data)
    except Exception as e:
        print(f"[ERROR] Schema validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("[RESULT] Schema validation PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main() 