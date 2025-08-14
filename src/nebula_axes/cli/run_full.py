#!/usr/bin/env python3
"""CLI for running full metrics analysis (axes + retention)"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd

from ..metrics.core import (
    compute_temporal_metrics,
    compute_drift_metrics,
    compute_shape_metrics,
    compute_density_metrics,
    compute_retention_metrics,
)


def compute_full_metrics(
    df_base: pd.DataFrame,
    df_shifted: Optional[pd.DataFrame] = None,
    feature_col: str = "feat_a",
    min_samples: int = 200,
) -> Dict[str, Any]:
    """Compute full metrics including axes and retention."""
    s = df_base[feature_col].astype(float)
    
    # Compute axes metrics
    print("Computing axes metrics...")
    temporal = compute_temporal_metrics(s)
    drift = compute_drift_metrics(s)
    shape = compute_shape_metrics(s)
    density = compute_density_metrics(df_base)
    
    axes_metrics = {**temporal, **drift, **shape, **density}
    
    # Compute retention metrics if shifted dataset provided
    retention_metrics = {}
    if df_shifted is not None:
        print("Computing retention metrics...")
        retention_metrics = compute_retention_metrics(
            df_base, df_shifted, min_samples=min_samples
        )
    
    # Combine all metrics
    full_metrics = {
        "metadata": {
            "version": "0.2.0",
            "analysis_type": "full_metrics",
            "base_samples": len(df_base),
            "shifted_samples": len(df_shifted) if df_shifted is not None else None,
            "feature_column": feature_col,
            "min_samples_required": min_samples,
        },
        "axes_metrics": axes_metrics,
        "retention_metrics": retention_metrics if retention_metrics else None,
    }
    
    return full_metrics


def main():
    """Main CLI entry point for full analysis."""
    parser = argparse.ArgumentParser(
        description="Compute full NebulaCon metrics (axes + retention)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Base dataset CSV file path"
    )
    parser.add_argument(
        "--shifted", "-s",
        type=str,
        help="Shifted dataset CSV file path (optional, for retention analysis)"
    )
    parser.add_argument(
        "--out", "-o",
        type=str,
        default="metrics/full_report.json",
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
        default=200,
        help="Minimum samples required for retention analysis"
    )
    parser.add_argument(
        "--json-out-dir",
        type=str,
        help="Directory for output files (creates if not exists)"
    )
    parser.add_argument(
        "--no-retention",
        action="store_true",
        help="Skip retention analysis even if shifted dataset provided"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    # Validate shifted file if provided
    df_shifted = None
    if args.shifted and not args.no_retention:
        shifted_path = Path(args.shifted)
        if not shifted_path.exists():
            print(f"Error: Shifted file not found: {shifted_path}")
            sys.exit(1)
    
    try:
        # Load base dataset
        print("Loading base dataset...")
        df_base = pd.read_csv(input_path)
        print(f"Base dataset: {len(df_base)} rows, {len(df_base.columns)} columns")
        
        # Load shifted dataset if provided
        if args.shifted and not args.no_retention:
            print("Loading shifted dataset...")
            df_shifted = pd.read_csv(args.shifted)
            print(f"Shifted dataset: {len(df_shifted)} rows, {len(df_shifted.columns)} columns")
        
        # Validate feature column
        if args.feature_col not in df_base.columns:
            print(f"Error: Feature column '{args.feature_col}' not found in base data")
            print(f"Available columns: {list(df_base.columns)}")
            sys.exit(1)
        
        # Check minimum samples
        if len(df_base) < 40:
            print(f"Warning: Base dataset has only {len(df_base)} samples (minimum: 40)")
        
        if df_shifted is not None and len(df_shifted) < args.min_samples:
            print(f"Warning: Shifted dataset has only {len(df_shifted)} samples (minimum: {args.min_samples})")
        
        # Compute full metrics
        print("Computing full metrics...")
        full_metrics = compute_full_metrics(
            df_base, df_shifted, args.feature_col, args.min_samples
        )
        
        # Prepare output
        output_path = Path(args.out)
        if args.json_out_dir:
            output_path = Path(args.json_out_dir) / output_path.name
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save results
        with open(output_path, "w") as f:
            json.dump(full_metrics, f, indent=2)
        
        print(f"✅ Full metrics computed successfully!")
        print(f"💾 Results saved to: {output_path}")
        
        # Print summary
        print("\n📊 Full Metrics Summary:")
        print(f"  Base samples: {full_metrics['metadata']['base_samples']}")
        print(f"  Shifted samples: {full_metrics['metadata']['shifted_samples']}")
        print(f"  Axes metrics: {len(full_metrics['axes_metrics'])}")
        print(f"  Retention metrics: {len(full_metrics['retention_metrics']) if full_metrics['retention_metrics'] else 0}")
        
        # Print key metrics
        print("\n🔑 Key Metrics:")
        axes = full_metrics['axes_metrics']
        for key in ['psi_trigger_rate', 'dip_stat', 'silhouette_approx']:
            if key in axes:
                value = axes[key]
                if value is not None:
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: None (insufficient data)")
                
    except Exception as e:
        print(f"Error computing full metrics: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 