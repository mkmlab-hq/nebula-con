import json
import pandas as pd
from utils.psi import population_stability_index

def compute_axes(df: pd.DataFrame):
    s = df["feat_a"].astype(float)
    global_var = float(s.var())
    roll_var = float(s.rolling(window=24, min_periods=5).var().mean())
    st_var_ratio = roll_var / (global_var + 1e-9)
    seasonal_corr = float(s.autocorr(lag=24))

    skew = float(s.skew())
    kurt = float(s.kurtosis())
    sk_k_score = abs(skew) + abs(kurt - 3)

    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = (q3 - q1) + 1e-9
    outlier_impact = float(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).mean())

    n = len(s)
    if n >= 100:
        psi_trigger_rate = population_stability_index(
            s.iloc[: n // 2], s.iloc[n // 2 :], bins=10, min_samples=50
        )
    else:
        psi_trigger_rate = 0.0

    return {
        "st_var_ratio": st_var_ratio,
        "seasonal_corr": seasonal_corr,
        "psi_trigger_rate": psi_trigger_rate,
        "sk_k_score": sk_k_score,
        "outlier_impact": outlier_impact,
        "dip_stat": None,  # TODO
        "intra_cluster_density": None,  # TODO (C축)
        "silhouette_approx": None,      # TODO
    }

if __name__ == "__main__":
    df = pd.read_csv("data/raw/sample.csv")
    metrics = compute_axes(df)
    with open("metrics/axes_run.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print("axes_run.json written") 