import pandas as pd
from typing import Optional
from ...utils.psi import population_stability_index  # 상대 경로로 수정

def compute_drift_metrics(s: pd.Series, *, min_len=120, bins=10, min_samples=50):
    n = len(s)
    if n < min_len:
        return {"psi_trigger_rate": 0.0}
    mid = n // 2
    baseline = s.iloc[:mid]
    current = s.iloc[mid:]
    psi = population_stability_index(baseline, current, bins=bins, min_samples=min_samples)
    return {"psi_trigger_rate": psi} 