"""
Tests for the FeatureBuilder class and A3 psi_trigger_rate calculation.
"""

import numpy as np
import pandas as pd
import pytest
from axes.feature_builder import FeatureBuilder, build_features_for_dataset


class TestFeatureBuilder:
    """Test cases for FeatureBuilder class."""
    
    def test_a3_psi_trigger_rate_with_drift(self):
        """Test A3 PSI trigger rate calculation with synthetic drift data."""
        # Create data with temporal drift
        np.random.seed(42)
        n_samples = 500
        
        # First half: normal distribution
        first_half = np.random.normal(0, 1, n_samples//2)
        # Second half: shifted distribution 
        second_half = np.random.normal(1, 1, n_samples//2)
        
        data = np.concatenate([first_half, second_half])
        
        builder = FeatureBuilder(window_size=50, psi_threshold=0.1)
        psi_rate = builder.calculate_a3_psi_trigger_rate(data)
        
        # Should detect drift - expect non-zero trigger rate
        assert isinstance(psi_rate, float)
        assert not np.isnan(psi_rate)
        assert psi_rate > 0
        
    def test_a3_psi_trigger_rate_stable(self):
        """Test A3 PSI trigger rate with stable data."""
        # Create stable data (same distribution throughout)
        np.random.seed(42)
        data = np.random.normal(0, 1, 500)
        
        # Use higher threshold for more realistic expectations with random data
        builder = FeatureBuilder(window_size=50, psi_threshold=0.2)
        psi_rate = builder.calculate_a3_psi_trigger_rate(data)
        
        # Should be lower trigger rate for stable data compared to drifted data
        assert isinstance(psi_rate, float)
        assert not np.isnan(psi_rate)
        assert 0.0 <= psi_rate <= 1.0  # Valid proportion
        
        # Compare with drifted data to ensure it's relatively lower
        # Create data with clear drift
        drift_first = np.random.normal(0, 1, 250)
        drift_second = np.random.normal(2, 1, 250)  # Clear shift
        drift_data = np.concatenate([drift_first, drift_second])
        
        drift_psi_rate = builder.calculate_a3_psi_trigger_rate(drift_data)
        
        # Drift data should have higher trigger rate than stable data
        assert drift_psi_rate > psi_rate
        
    def test_a3_psi_trigger_rate_with_nans(self):
        """Test A3 PSI trigger rate with NaN values."""
        np.random.seed(42)
        data = np.random.normal(0, 1, 300)
        
        # Add some NaN values
        data[::10] = np.nan
        
        builder = FeatureBuilder(window_size=50, psi_threshold=0.1)
        psi_rate = builder.calculate_a3_psi_trigger_rate(data)
        
        # Should handle NaN values gracefully
        assert isinstance(psi_rate, float)
        # May be NaN if too much data is missing, but should not error
        
    def test_a3_psi_trigger_rate_insufficient_data(self):
        """Test A3 PSI trigger rate with insufficient data."""
        # Too little data for analysis
        data = np.random.normal(0, 1, 40)
        
        builder = FeatureBuilder(window_size=50, psi_threshold=0.1)
        psi_rate = builder.calculate_a3_psi_trigger_rate(data)
        
        # Should return 0.0 for insufficient data (graceful handling)
        assert psi_rate == 0.0
        
    def test_calculate_axes_features(self):
        """Test full axes features calculation."""
        np.random.seed(42)
        data = np.random.normal(0, 1, 300)
        
        builder = FeatureBuilder()
        features = builder.calculate_axes_features(data)
        
        # Check that all expected features are present
        expected_features = [
            'A3_psi_trigger_rate', 'A1_st_var_ratio', 'A2_seasonal_corr',
            'B1_sk_k_score', 'B2_outlier_impact', 'B3_dip_stat',
            'C1_intra_cluster_dist', 'C2_silhouette', 'C3_mutual_info_reduction',
            'D1_loss_retention_ratio', 'D2_steps_to_plateau', 'D3_leak_score'
        ]
        
        for feature in expected_features:
            assert feature in features
            
        # A3 should be implemented (not NaN for sufficient data)
        assert not np.isnan(features['A3_psi_trigger_rate'])
        
        # Others should be NaN (not implemented)
        for feature in expected_features[1:]:
            assert np.isnan(features[feature])
            
    def test_build_features_for_dataset_function(self):
        """Test the convenience function."""
        np.random.seed(42)
        data = pd.DataFrame({
            'values': np.random.normal(0, 1, 300),
            'other': np.random.normal(1, 1, 300)
        })
        
        features = build_features_for_dataset(data, 'values')
        
        assert 'A3_psi_trigger_rate' in features
        assert not np.isnan(features['A3_psi_trigger_rate'])
        
    def test_dataframe_input_auto_column_selection(self):
        """Test auto-selection of numeric column from DataFrame."""
        np.random.seed(42)
        data = pd.DataFrame({
            'text': ['a', 'b', 'c'] * 100,
            'numeric': np.random.normal(0, 1, 300),
            'another_numeric': np.random.normal(1, 1, 300)
        })
        
        builder = FeatureBuilder()
        # Should auto-select first numeric column
        psi_rate = builder.calculate_a3_psi_trigger_rate(data)
        
        assert isinstance(psi_rate, float)
        assert not np.isnan(psi_rate)