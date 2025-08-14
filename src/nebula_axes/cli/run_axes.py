#!/usr/bin/env python3
"""CLI for running axes metrics analysis"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from ..metrics.core import (
    compute_temporal_metrics,
    compute_drift_metrics,
    compute_shape_metrics,
    compute_density_metrics,
)


def compute_axes(df: pd.DataFrame, feature_col: str = "feat_a") -> dict:
    """Compute all axes metrics for a dataset."""
    s = df[feature_col].astype(float)
    
    # Compute metrics for each axis
    temporal = compute_temporal_metrics(s)
    drift = compute_drift_metrics(s)
    shape = compute_shape_metrics(s)
    density = compute_density_metrics(df)
    
    # Combine all metrics
    metrics = {**temporal, **drift, **shape, **density}
    return metrics


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compute NebulaCon axes metrics for a dataset",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default="data/raw/sample.csv",
        help="Input CSV file path"
    )
    parser.add_argument(
        "--out", "-o",
        type=str,
        default="metrics/axes_run.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--feature-col", "-f",
        type=str,
        default="feat_a",
        help="Feature column name to analyze"
    )
    parser.add_argument(
        "--min-samples",
        type=int,
        default=40,
        help="Minimum samples required for analysis"
    )
    parser.add_argument(
        "--json-out-dir",
        type=str,
        help="Directory for output files (creates if not exists)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    try:
        # Load data
        df = pd.read_csv(input_path)
        print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
        
        # Validate feature column
        if args.feature_col not in df.columns:
            print(f"Error: Feature column '{args.feature_col}' not found in data")
            print(f"Available columns: {list(df.columns)}")
            sys.exit(1)
        
        # Check minimum samples
        if len(df) < args.min_samples:
            print(f"Warning: Only {len(df)} samples (minimum: {args.min_samples})")
        
        # Compute metrics
        print("Computing axes metrics...")
        metrics = compute_axes(df, args.feature_col)
        
        # Prepare output
        output_path = Path(args.out)
        if args.json_out_dir:
            output_path = Path(args.json_out_dir) / output_path.name
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save results
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)
        
        print(f"✅ Axes metrics computed successfully!")
        print(f"📊 Total metrics: {len(metrics)}")
        print(f"💾 Results saved to: {output_path}")
        
        # Print summary
        print("\n📈 Metrics Summary:")
        for key, value in metrics.items():
            if value is not None:
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: None (insufficient data)")
                
    except Exception as e:
        print(f"Error computing metrics: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 