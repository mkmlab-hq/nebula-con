from typing import Optional
import numpy as np

def approximate_dip(x: np.ndarray, grid_size: int = 256) -> Optional[float]:
    """
    Approximate Hartigan Dip Test for unimodality detection.

    Args:
        x: Input data array
        grid_size: Number of grid points for KDE estimation

    Returns:
        float: Dip statistic (0 = unimodal, >0.02 = potentially multimodal)
        None: Insufficient data
    """
    # Convert to numpy array and remove NaN
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]

    # Edge cases
    if len(x) < 40:
        return None
    if len(np.unique(x)) < 3:
        return 0.0

    # Create evaluation grid
    x_min, x_max = np.min(x), np.max(x)
    if x_max == x_min:
        return 0.0
    grid = np.linspace(x_min, x_max, grid_size)

    # Simple KDE estimation (Gaussian kernel)
    bandwidth = np.std(x) * (len(x) ** (-1 / 5))  # Scott's rule approximation
    kde_values = np.zeros_like(grid)
    for i, point in enumerate(grid):
        kernel_values = np.exp(-0.5 * ((x - point) / bandwidth) ** 2)
        kde_values[i] = np.mean(kernel_values) / bandwidth

    # Find peaks and valleys
    diff = np.diff(kde_values)
    sign_changes = np.diff(np.sign(diff))
    peaks = np.sum(sign_changes < 0)
    # valleys = np.sum(sign_changes > 0)  # 미사용 변수

    # Handle edge cases
    if peaks <= 1:
        return 0.0  # Unimodal

    # Calculate valley depth
    local_min_indices = np.where(sign_changes > 0)[0]
    local_max_indices = np.where(sign_changes < 0)[0]
    if len(local_min_indices) == 0 or len(local_max_indices) == 0:
        return 0.0
    valley_depths = []
    for valley_idx in local_min_indices:
        left_peaks = local_max_indices[local_max_indices < valley_idx]
        right_peaks = local_max_indices[local_max_indices > valley_idx]
        if len(left_peaks) > 0 and len(right_peaks) > 0:
            left_peak_val = kde_values[left_peaks[-1]]
            right_peak_val = kde_values[right_peaks[0]]
            valley_val = kde_values[valley_idx]
            avg_peak = (left_peak_val + right_peak_val) / 2
            if avg_peak > 0:
                depth = (avg_peak - valley_val) / avg_peak
                valley_depths.append(depth)
    if not valley_depths:
        return 0.0
    avg_valley_depth = np.mean(valley_depths)
    global_max = np.max(kde_values)
    normalized_depth = avg_valley_depth / global_max if global_max > 0 else avg_valley_depth
    normalized_depth = np.clip(normalized_depth, 0, 1)
    dip_stat = normalized_depth * (peaks - 1) * 0.5
    return float(dip_stat)

def dip_test_unimodal(x: np.ndarray, threshold: float = 0.02) -> bool:
    """
    Simple unimodality test using dip statistic.

    Args:
        x: Input data array
        threshold: Maximum dip value for unimodal (default: 0.02)

    Returns:
        bool: True if unimodal, False if potentially multimodal
    """
    dip_val = approximate_dip(x)
    if dip_val is None:
        return True  # Assume unimodal for insufficient data
    return dip_val <= threshold