import pandas as pd

def compute_temporal_metrics(s: pd.Series, *, window=24, min_periods=5, seasonal_lag=24):
    s = pd.to_numeric(s, errors="coerce")
    global_var = float(s.var())
    rolling_var = float(s.rolling(window=window, min_periods=min_periods).var().mean())
    st_var_ratio = rolling_var / (global_var + 1e-9)
    seasonal_corr = float(s.autocorr(lag=seasonal_lag))
    return {
        "st_var_ratio": st_var_ratio,
        "seasonal_corr": seasonal_corr
    } 