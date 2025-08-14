#!/usr/bin/env python3
"""Test script for new modular metrics structure"""

import sys
sys.path.append('.')

from metrics.core import (
    compute_temporal_metrics,
    compute_drift_metrics,
    compute_shape_metrics,
    compute_density_metrics
)
import pandas as pd

def main():
    print("Testing new modular metrics structure...")
    
    # Load sample data
    df = pd.read_csv('data/raw/sample.csv')
    s = df['feat_a'].astype(float)
    
    print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"Feature 'feat_a' range: {s.min():.4f} to {s.max():.4f}")
    
    # Test each module
    print("\n=== Testing Core Modules ===")
    
    # Temporal metrics (A-axis)
    temporal = compute_temporal_metrics(s)
    print(f"Temporal: {temporal}")
    
    # Drift metrics (A-axis)
    drift = compute_drift_metrics(s)
    print(f"Drift: {drift}")
    
    # Shape metrics (B-axis)
    shape = compute_shape_metrics(s)
    print(f"Shape: {shape}")
    
    # Density metrics (C-axis)
    density = compute_density_metrics(df)
    print(f"Density: {density}")
    
    # Combine all metrics
    all_metrics = {**temporal, **drift, **shape, **density}
    print(f"\n=== Combined Metrics ({len(all_metrics)} total) ===")
    for key, value in all_metrics.items():
        print(f"  {key}: {value}")
    
    print("\n✅ New structure test completed successfully!")

if __name__ == "__main__":
    main() 