"""
Population Stability Index (PSI) calculation utilities for NebulaCon.

PSI measures the shift in the distribution of a variable between two datasets,
typically used to monitor model drift over time.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional


def population_stability_index(
    expected: Union[np.ndarray, pd.Series], 
    actual: Union[np.ndarray, pd.Series], 
    bins: int = 10
) -> float:
    """
    Calculate Population Stability Index (PSI) between expected and actual distributions.
    
    PSI = sum((actual_pct - expected_pct) * ln(actual_pct / expected_pct))
    
    Args:
        expected: Expected/baseline distribution (reference data)
        actual: Actual distribution (new data to compare)
        bins: Number of quantile bins to use (default: 10)
        
    Returns:
        float: PSI value. Higher values indicate greater distribution shift.
               Values > 0.1 typically indicate significant drift.
               
    Raises:
        ValueError: If inputs are empty or contain only NaN values
    """
    # Convert to numpy arrays and handle NaN values
    expected_arr = np.asarray(expected)
    actual_arr = np.asarray(actual)
    
    # Remove NaN values
    expected_clean = expected_arr[~np.isnan(expected_arr)]
    actual_clean = actual_arr[~np.isnan(actual_arr)]
    
    # Check if we have valid data
    if len(expected_clean) == 0 or len(actual_clean) == 0:
        return np.nan
    
    # Check for constant values (no variance)
    if np.var(expected_clean) == 0 and np.var(actual_clean) == 0:
        if np.all(expected_clean == actual_clean[0]):
            return 0.0  # Same constant value
        else:
            return np.inf  # Different constant values
    
    # Create quantile bins based on expected data
    if np.var(expected_clean) == 0:
        # Expected data is constant - use actual data for binning
        _, bin_edges = np.histogram(actual_clean, bins=bins)
    else:
        # Use expected data quantiles for binning
        bin_edges = np.percentile(expected_clean, np.linspace(0, 100, bins + 1))
        # Ensure unique bin edges
        bin_edges = np.unique(bin_edges)
        if len(bin_edges) < 2:
            return np.nan
    
    # Make sure we have proper bin edges
    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf
    
    # Calculate histograms
    expected_counts, _ = np.histogram(expected_clean, bins=bin_edges)
    actual_counts, _ = np.histogram(actual_clean, bins=bin_edges)
    
    # Convert to percentages
    expected_pct = expected_counts / len(expected_clean)
    actual_pct = actual_counts / len(actual_clean)
    
    # Handle zero percentages by adding small epsilon
    epsilon = 1e-10
    expected_pct = np.maximum(expected_pct, epsilon)
    actual_pct = np.maximum(actual_pct, epsilon)
    
    # Calculate PSI
    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    
    return float(psi)