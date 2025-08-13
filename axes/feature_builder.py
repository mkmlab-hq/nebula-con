"""
Feature builder for NebulaCon Universal Pattern Axes (UPA).

This module implements the 4x3 axes framework for measuring dataset characteristics:
- A: Temporal Stability  
- B: Distributional Shape
- C: Semantic Density
- D: Cross-Domain Transferability

Each macro axis has 3 micro axes (A1-A3, B1-B3, etc.).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union
from utils.psi import population_stability_index


class FeatureBuilder:
    """
    Builder for NebulaCon Universal Pattern Axes features.
    
    Implements micro-axes calculations for the 4x3 UPA framework.
    """
    
    def __init__(self, window_size: int = 100, psi_threshold: float = 0.1):
        """
        Initialize the feature builder.
        
        Args:
            window_size: Size of rolling windows for temporal analysis
            psi_threshold: PSI threshold for detecting distribution drift
        """
        self.window_size = window_size
        self.psi_threshold = psi_threshold
        
    def calculate_a3_psi_trigger_rate(
        self, 
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        column: Optional[str] = None
    ) -> float:
        """
        Calculate A3 psi_trigger_rate: Proportion of windows with synthetic PSI > threshold.
        
        This metric measures temporal stability by calculating PSI between rolling windows
        and the overall distribution, then computing the proportion of windows that exceed
        the drift threshold.
        
        Args:
            data: Input data (DataFrame, Series, or array)
            column: Column name if data is DataFrame
            
        Returns:
            float: Proportion of windows with PSI > threshold (0.0 to 1.0)
                   Returns NaN if calculation is not possible
        """
        # Convert input to pandas Series for consistent handling
        if isinstance(data, pd.DataFrame):
            if column is None:
                # Use first numeric column if no column specified
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    return np.nan
                column = numeric_cols[0]
            series = data[column]
        elif isinstance(data, pd.Series):
            series = data
        else:
            series = pd.Series(data)
            
        # Remove NaN values for baseline calculation but keep track of positions
        original_length = len(series)
        clean_data = series.dropna()
        
        if len(clean_data) < 50:
            # Graceful: if fewer than 50 rows → psi_trigger_rate = 0.0
            return 0.0
            
        # Check if all values are the same → psi_trigger_rate = 0.0
        if np.var(clean_data) == 0:
            return 0.0
            
        # Use the clean data as baseline (expected distribution)
        baseline = clean_data.values
        
        # Calculate rolling windows
        windows_above_threshold = 0
        total_windows = 0
        
        # Generate rolling windows
        for i in range(len(clean_data) - self.window_size + 1):
            window_data = clean_data.iloc[i:i + self.window_size].values
            
            # Skip windows with insufficient data
            if len(window_data) < self.window_size * 0.8:  # Allow up to 20% missing
                continue
                
            # Calculate PSI between window and baseline
            try:
                psi_value = population_stability_index(baseline, window_data, bins=10)
                
                # Check if PSI is valid and above threshold
                if not np.isnan(psi_value) and not np.isinf(psi_value):
                    total_windows += 1
                    if psi_value > self.psi_threshold:
                        windows_above_threshold += 1
                        
            except Exception:
                # Skip windows that cause calculation errors
                continue
                
        # Calculate trigger rate
        if total_windows == 0:
            return 0.0
            
        trigger_rate = windows_above_threshold / total_windows
        return float(trigger_rate)
        
    def calculate_axes_features(
        self, 
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        column: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate all implemented axes features.
        
        Args:
            data: Input data
            column: Column name if data is DataFrame
            
        Returns:
            Dict with calculated feature values
        """
        features = {}
        
        # A3: PSI trigger rate (implemented)
        features['A3_psi_trigger_rate'] = self.calculate_a3_psi_trigger_rate(data, column)
        
        # Placeholder for other axes (not yet implemented)
        features['A1_st_var_ratio'] = np.nan
        features['A2_seasonal_corr'] = np.nan
        features['B1_sk_k_score'] = np.nan
        features['B2_outlier_impact'] = np.nan
        features['B3_dip_stat'] = np.nan
        features['C1_intra_cluster_dist'] = np.nan
        features['C2_silhouette'] = np.nan
        features['C3_mutual_info_reduction'] = np.nan
        features['D1_loss_retention_ratio'] = np.nan
        features['D2_steps_to_plateau'] = np.nan
        features['D3_leak_score'] = np.nan
        
        return features


def build_features_for_dataset(
    data: Union[pd.DataFrame, pd.Series, np.ndarray],
    column: Optional[str] = None,
    **kwargs
) -> Dict[str, float]:
    """
    Convenience function to build all features for a dataset.
    
    Args:
        data: Input data
        column: Column name if data is DataFrame
        **kwargs: Additional arguments for FeatureBuilder
        
    Returns:
        Dict with all calculated features
    """
    builder = FeatureBuilder(**kwargs)
    return builder.calculate_axes_features(data, column)