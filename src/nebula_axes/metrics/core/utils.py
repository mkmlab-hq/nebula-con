import numpy as np
import pandas as pd
from typing import Optional

def series_float(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

def safe_var(s: pd.Series) -> float:
    v = s.var()
    return float(v) if np.isfinite(v) else 0.0

def half_split(s: pd.Series):
    n = len(s)
    mid = n // 2
    return s.iloc[:mid], s.iloc[mid:]

def guard_min_len(arr, min_len: int) -> bool:
    return len(arr) >= min_len

def safe_ratio(a: float, b: float, eps=1e-9) -> float:
    return float(a) / (float(b) + eps)

def try_or_none(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None

def approximate_quantile_bins(x: np.ndarray, bins: int):
    qs = np.linspace(0, 1, bins + 1)
    return np.unique(np.quantile(x, qs)) 