import numpy as np
import pytest
from utils.dip import approximate_dip, dip_test_unimodal

def test_dip_unimodal():
    """Test dip statistic with unimodal (normal) distribution"""
    np.random.seed(0)
    x = np.random.normal(0, 1, 200)
    
    dip_val = approximate_dip(x)
    
    assert dip_val is not None
    assert dip_val < 0.02  # Should be unimodal
    assert dip_val >= 0.0

def test_dip_bimodal_clear():
    """Test dip statistic with clear bimodal distribution"""
    np.random.seed(1)
    # Create clear bimodal distribution
    x1 = np.random.normal(-2, 0.4, 100)
    x2 = np.random.normal(2, 0.4, 100)
    x = np.concatenate([x1, x2])
    
    dip_val = approximate_dip(x)
    
    assert dip_val is not None
    assert dip_val > 0.05  # Should detect bimodality
    assert dip_val < 1.0   # Should be reasonable range

def test_dip_small_sample():
    """Test dip statistic with insufficient samples"""
    np.random.seed(2)
    x = np.random.normal(0, 1, 30)  # < 40 samples
    
    dip_val = approximate_dip(x)
    
    assert dip_val is None  # Should return None for small samples

def test_dip_plateau():
    """Test dip statistic with uniform distribution (plateau)"""
    np.random.seed(3)
    x = np.random.uniform(0, 1, 200)
    
    dip_val = approximate_dip(x)
    
    assert dip_val is not None
    assert dip_val < 0.02  # Uniform should appear unimodal

def test_dip_edge_cases():
    """Test dip statistic edge cases"""
    # Single value repeated
    x_single = np.array([1.0] * 100)
    dip_val = approximate_dip(x_single)
    assert dip_val == 0.0
    
    # Two unique values
    x_two = np.array([1.0, 2.0] * 50)
    dip_val = approximate_dip(x_two)
    assert dip_val == 0.0
    
    # NaN values
    x_nan = np.array([1.0, 2.0, np.nan, 3.0, 4.0] * 40)
    dip_val = approximate_dip(x_nan)
    assert dip_val is not None
    assert dip_val >= 0.0

def test_dip_test_unimodal():
    """Test the simple unimodality test function"""
    np.random.seed(4)
    
    # Unimodal case
    x_unimodal = np.random.normal(0, 1, 200)
    is_unimodal = dip_test_unimodal(x_unimodal)
    assert is_unimodal == True
    
    # Bimodal case
    x1 = np.random.normal(-2, 0.4, 100)
    x2 = np.random.normal(2, 0.4, 100)
    x_bimodal = np.concatenate([x1, x2])
    is_unimodal = dip_test_unimodal(x_bimodal)
    assert is_unimodal == False
    
    # Small sample case
    x_small = np.random.normal(0, 1, 30)
    is_unimodal = dip_test_unimodal(x_small)
    assert is_unimodal == True  # Assumes unimodal for insufficient data

def test_dip_performance():
    """Test dip statistic performance with larger datasets"""
    np.random.seed(5)
    x = np.random.normal(0, 1, 1000)
    
    dip_val = approximate_dip(x)
    
    assert dip_val is not None
    assert dip_val >= 0.0
    assert dip_val < 1.0
    
    # Should complete in reasonable time
    import time
    start_time = time.time()
    approximate_dip(x)
    end_time = time.time()
    
    assert (end_time - start_time) < 1.0  # Should complete in < 1 second 