import numpy as np
from typing import Optional

def population_stability_index(expected, actual, bins=10, min_samples=50):
    """Calculate Population Stability Index (PSI) between two distributions."""
    # Convert to numpy arrays and handle edge cases
    expected = np.array(expected, dtype=float)
    actual = np.array(actual, dtype=float)
    
    # Remove NaN values
    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]
    
    # Check minimum sample requirements
    if len(expected) < min_samples or len(actual) < min_samples:
        return 0.0
    
    # Handle identical distributions
    if np.array_equal(expected, actual):
        return 0.0
    
    # Find global min/max for consistent binning
    global_min = min(np.min(expected), np.min(actual))
    global_max = max(np.max(expected), np.max(actual))
    
    # Handle edge case where all values are identical
    if global_min == global_max:
        return 0.0
    
    # Create bins with small epsilon to avoid edge issues
    epsilon = 1e-10
    bin_edges = np.linspace(global_min - epsilon, global_max + epsilon, bins + 1)
    
    # Calculate histograms
    expected_hist, _ = np.histogram(expected, bins=bin_edges)
    actual_hist, _ = np.histogram(actual, bins=bin_edges)
    
    # Add small constant to avoid division by zero
    expected_hist = expected_hist.astype(float) + 1e-10
    actual_hist = actual_hist.astype(float) + 1e-10
    
    # Normalize to probabilities
    expected_p = expected_hist / np.sum(expected_hist)
    actual_p = actual_hist / np.sum(actual_hist)
    
    # Calculate PSI
    psi = 0.0
    for i in range(len(expected_p)):
        if expected_p[i] > 0 and actual_p[i] > 0:
            psi += (actual_p[i] - expected_p[i]) * np.log(actual_p[i] / expected_p[i])
    
    return float(psi) 