import numpy as np
import pytest
from utils.density import compute_density_metrics

def test_density_well_separated():
    """Test density metrics with well-separated clusters"""
    np.random.seed(0)
    # Create two well-separated clusters
    a = np.random.normal(0, 0.3, (100, 2))
    b = np.random.normal(3, 0.3, (100, 2))
    X = np.vstack([a, b])
    
    intra, sil, k = compute_density_metrics(X)
    
    assert sil is not None and sil > 0.3  # Good separation
    assert intra is not None and intra < 0.7  # Low intra-cluster density
    assert k is not None and k >= 2

def test_density_single_cloud():
    """Test density metrics with single Gaussian cloud"""
    np.random.seed(1)
    X = np.random.normal(0, 1, (150, 2))
    
    intra, sil, k = compute_density_metrics(X)
    
    # Single cloud may still show some structure
    assert sil is not None and sil < 0.5  # Relaxed threshold
    assert intra is not None
    assert k is not None

def test_density_insufficient_samples():
    """Test with insufficient samples"""
    X = np.random.normal(0, 1, (30, 2))  # < min_samples=40
    
    intra, sil, k = compute_density_metrics(X)
    
    assert intra is None
    assert sil is None
    assert k is None

def test_density_single_feature():
    """Test with single feature (insufficient dimensions)"""
    X = np.random.normal(0, 1, (100, 1))  # Only 1 feature
    
    intra, sil, k = compute_density_metrics(X)
    
    assert intra is None
    assert sil is None
    assert k is None

def test_density_with_nan():
    """Test with NaN values"""
    np.random.seed(2)
    X = np.random.normal(0, 1, (100, 3))
    X[10, 0] = np.nan  # Add some NaN values
    
    intra, sil, k = compute_density_metrics(X)
    
    assert intra is not None  # Should handle NaN removal
    assert sil is not None
    assert k is not None

def test_density_edge_cases():
    """Test edge cases"""
    # Empty array
    X_empty = np.array([]).reshape(0, 2)
    intra, sil, k = compute_density_metrics(X_empty)
    assert intra is None
    
    # None input
    intra, sil, k = compute_density_metrics(None)
    assert intra is None
    
    # 1D array
    X_1d = np.random.normal(0, 1, 100)
    intra, sil, k = compute_density_metrics(X_1d)
    assert intra is None 