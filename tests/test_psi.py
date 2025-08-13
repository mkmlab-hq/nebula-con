"""
Tests for PSI (Population Stability Index) calculation utilities.

Tests cover three main scenarios:
1. Normal distribution data
2. All same values (constant data)
3. Data with partial NaN values
"""

import numpy as np
import pandas as pd
import pytest
from utils.psi import population_stability_index


class TestPSI:
    """Test cases for Population Stability Index calculation."""
    
    def test_normal_distribution(self):
        """Test PSI calculation with normal distribution data."""
        # Generate two normal distributions with slight difference
        np.random.seed(42)
        expected = np.random.normal(0, 1, 1000)
        actual = np.random.normal(0.1, 1.1, 1000)  # Slightly shifted and scaled
        
        psi = population_stability_index(expected, actual, bins=10)
        
        # PSI should be a positive number for different distributions
        assert isinstance(psi, float)
        assert not np.isnan(psi)
        assert not np.isinf(psi)
        assert psi > 0
        
        # For similar but not identical distributions, PSI should be moderate
        assert 0.01 < psi < 1.0
        
    def test_identical_distributions(self):
        """Test PSI calculation with identical distributions."""
        np.random.seed(42)
        data = np.random.normal(0, 1, 1000)
        
        psi = population_stability_index(data, data, bins=10)
        
        # PSI should be very close to 0 for identical distributions
        assert isinstance(psi, float)
        assert not np.isnan(psi)
        assert psi < 1e-10  # Should be essentially zero
        
    def test_all_same_values(self):
        """Test PSI calculation when all values are the same."""
        # Case 1: Both datasets have the same constant value
        expected = np.full(100, 5.0)
        actual = np.full(100, 5.0)
        
        psi = population_stability_index(expected, actual, bins=10)
        assert psi == 0.0
        
        # Case 2: Different constant values
        expected = np.full(100, 5.0)
        actual = np.full(100, 7.0)
        
        psi = population_stability_index(expected, actual, bins=10)
        assert np.isinf(psi)  # Should be infinite for completely different constants
        
    def test_partial_nan_values(self):
        """Test PSI calculation with data containing NaN values."""
        np.random.seed(42)
        
        # Create datasets with some NaN values
        expected = np.random.normal(0, 1, 1000)
        actual = np.random.normal(0.1, 1.1, 1000)
        
        # Introduce NaN values
        expected[::10] = np.nan  # Every 10th value is NaN
        actual[::15] = np.nan    # Every 15th value is NaN
        
        psi = population_stability_index(expected, actual, bins=10)
        
        # Should handle NaN values gracefully
        assert isinstance(psi, float)
        assert not np.isnan(psi)
        assert not np.isinf(psi)
        assert psi > 0
        
    def test_all_nan_values(self):
        """Test PSI calculation when all values are NaN."""
        expected = np.full(100, np.nan)
        actual = np.full(100, np.nan)
        
        psi = population_stability_index(expected, actual, bins=10)
        assert np.isnan(psi)
        
    def test_empty_arrays(self):
        """Test PSI calculation with empty arrays."""
        expected = np.array([])
        actual = np.array([])
        
        psi = population_stability_index(expected, actual, bins=10)
        assert np.isnan(psi)
        
    def test_pandas_series_input(self):
        """Test PSI calculation with pandas Series input."""
        np.random.seed(42)
        expected = pd.Series(np.random.normal(0, 1, 1000))
        actual = pd.Series(np.random.normal(0.1, 1.1, 1000))
        
        psi = population_stability_index(expected, actual, bins=10)
        
        assert isinstance(psi, float)
        assert not np.isnan(psi)
        assert not np.isinf(psi)
        assert psi > 0