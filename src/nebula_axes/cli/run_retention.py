#!/usr/bin/env python3
"""CLI for running retention metrics analysis"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from ..metrics.core import compute_retention_metrics


def main():
    """Main CLI entry point for retention analysis."""
    parser = argparse.ArgumentParser(
        description="Compute NebulaCon retention metrics between base and shifted datasets",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--base", "-b",
        type=str,
        required=True,
        help="Base dataset CSV file path"
    )
    parser.add_argument(
        "--shifted", "-s",
        type=str,
        required=True,
        help="Shifted dataset CSV file path"
    )
    parser.add_argument(
        "--out", "-o",
        type=str,
        default="metrics/retention_run.json",
        help="Output JSON file path"
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
    
    args = parser.parse_args()
    
    # Validate input files
    base_path = Path(args.base)
    shifted_path = Path(args.shifted)
    
    if not base_path.exists():
        print(f"Error: Base file not found: {base_path}")
        sys.exit(1)
    
    if not shifted_path.exists():
        print(f"Error: Shifted file not found: {shifted_path}")
        sys.exit(1)
    
    try:
        # Load datasets
        print("Loading datasets...")
        df_base = pd.read_csv(base_path)
        df_shifted = pd.read_csv(shifted_path)
        
        print(f"Base dataset: {len(df_base)} rows, {len(df_base.columns)} columns")
        print(f"Shifted dataset: {len(df_shifted)} rows, {len(df_shifted.columns)} columns")
        
        # Validate column compatibility
        if list(df_base.columns) != list(df_shifted.columns):
            print("Warning: Column mismatch between base and shifted datasets")
            print(f"Base columns: {list(df_base.columns)}")
            print(f"Shifted columns: {list(df_shifted.columns)}")
        
        # Check minimum samples
        if len(df_base) < args.min_samples:
            print(f"Warning: Base dataset has only {len(df_base)} samples (minimum: {args.min_samples})")
        
        if len(df_shifted) < args.min_samples:
            print(f"Warning: Shifted dataset has only {len(df_shifted)} samples (minimum: {args.min_samples})")
        
        # Compute retention metrics
        print("Computing retention metrics...")
        metrics = compute_retention_metrics(df_base, df_shifted, min_samples=args.min_samples)
        
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
        
        print(f"✅ Retention metrics computed successfully!")
        print(f"💾 Results saved to: {output_path}")
        
        # Print summary
        print("\n📊 Retention Summary:")
        for key, value in metrics.items():
            if value is not None:
                if "retention" in key and isinstance(value, float):
                    print(f"  {key}: {value:.4f} ({value*100:.1f}%)")
                else:
                    print(f"  {key}: {value}")
            else:
                print(f"  {key}: None (insufficient data)")
                
    except Exception as e:
        print(f"Error computing retention metrics: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 