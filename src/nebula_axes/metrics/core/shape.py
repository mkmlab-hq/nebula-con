import numpy as np
import pandas as pd
from ...utils.dip import approximate_dip  # 상대 경로로 수정

def compute_shape_metrics(s: pd.Series):
    s = pd.to_numeric(s, errors="coerce")
    skew = float(s.skew())
    kurt = float(s.kurtosis())
    sk_k_score = abs(skew) + abs(kurt - 3)
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = (q3 - q1) + 1e-9
    outlier_impact = float(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).mean())
    dip_stat = approximate_dip(s.values)
    return {
        "sk_k_score": sk_k_score,
        "outlier_impact": outlier_impact,
        "dip_stat": dip_stat
    } 