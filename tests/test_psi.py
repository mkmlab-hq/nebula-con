import pytest
import numpy as np
import pandas as pd
from utils.psi import population_stability_index

def test_psi_positive_values():
    """Test PSI with positive values"""
    baseline = np.random.normal(10, 2, 100)
    current = np.random.normal(12, 2, 100)  # Shifted distribution
    psi = population_stability_index(baseline, current)
    assert psi > 0
    assert isinstance(psi, float)

def test_psi_identical_distributions():
    """Test PSI with identical distributions"""
    data = np.random.normal(0, 1, 100)
    psi = population_stability_index(data, data)
    assert psi == 0.0

def test_psi_with_nan_values():
    """Test PSI with NaN values"""
    baseline = np.array([1, 2, np.nan, 4, 5])
    current = np.array([1, 2, 3, 4, 5])
    psi = population_stability_index(baseline, current)
    assert isinstance(psi, float)
    assert not np.isnan(psi)

def test_psi_small_sample():
    """Test PSI with small sample size"""
    baseline = np.random.normal(0, 1, 30)
    current = np.random.normal(0, 1, 30)
    psi = population_stability_index(baseline, current, min_samples=50)
    assert psi == 0.0

def test_psi_edge_cases():
    """Test PSI edge cases"""
    # Single value repeated
    baseline = np.array([1.0] * 100)
    current = np.array([1.0] * 100)
    psi = population_stability_index(baseline, current)
    assert psi == 0.0
    
    # Different single values
    baseline = np.array([1.0] * 100)
    current = np.array([2.0] * 100)
    psi = population_stability_index(baseline, current)
    assert psi > 0 