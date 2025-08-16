from typing import Any, Dict

import numpy as np
import pandas as pd


class AxesFeatureBuilder:
    def __init__(self, cfg: Dict[str, Any] | None = None):
        self.cfg = cfg or {}

    def temporal_metrics(self, df: pd.DataFrame, time_col: str, target_col: str) -> Dict[str, float]:
        s = df.sort_values(time_col)[target_col].astype(float)
        if len(s) < 30:
            return {"st_var_ratio": np.nan, "seasonal_corr": np.nan, "psi_trigger_rate": np.nan}
        global_var = float(s.var())
        win = min(24, max(5, len(s)//10))
        roll_var = float(s.rolling(window=win, min_periods=5).var().mean())
        st_var_ratio = roll_var / (global_var + 1e-9)
        lag = min(24, max(2, len(s)//12))
        seasonal_corr = s.autocorr(lag=lag)

        # A3: REAL PSI calculation
        n = len(s)
        if n >= 120:
            mid = n // 2
            baseline = s.iloc[:mid]
            current = s.iloc[mid:]
            from utils.psi import population_stability_index
            psi_trigger_rate = population_stability_index(
                baseline, current, bins=10, min_samples=50
            )
        else:
            psi_trigger_rate = 0.0  # 데이터가 너무 적을 때는 변화 감지 무효

        return {
            "st_var_ratio": st_var_ratio,
            "seasonal_corr": float(seasonal_corr) if seasonal_corr is not None else np.nan,
            "psi_trigger_rate": psi_trigger_rate
        }

    def distributional_metrics(self, series: pd.Series) -> Dict[str, float]:
        s = series.astype(float).dropna()
        skew = s.skew()
        kurt = s.kurtosis()
        sk_k_score = float(abs(skew) + abs(kurt - 3))
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = (q3 - q1) + 1e-9
        outlier_impact = float(((s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)).mean())
        dip_stat = np.nan  # placeholder for future Hartigan dip test
        return {
            "sk_k_score": sk_k_score,
            "outlier_impact": outlier_impact,
            "dip_stat": dip_stat
        }

    def build(self, df: pd.DataFrame, time_col: str, target_col: str) -> Dict[str, float]:
        t = self.temporal_metrics(df, time_col, target_col)
        d = self.distributional_metrics(df[target_col])
        return {**t, **d}

if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--time_col", default=None)
    ap.add_argument("--target_col", default=None)
    args = ap.parse_args()
    df = pd.read_csv(args.data)
    if not args.time_col:
        args.time_col = df.columns[0]
    if not args.target_col:
        args.target_col = df.columns[-1]
    fb = AxesFeatureBuilder()
    feats = fb.build(df, args.time_col, args.target_col)
    print(json.dumps(feats, indent=2))
