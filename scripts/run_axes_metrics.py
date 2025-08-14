import json
import pandas as pd
from utils.psi import population_stability_index
from utils.density import compute_density_metrics

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

    # A3: REAL PSI calculation
    n = len(s)
    if n >= 120:
        mid = n // 2
        baseline = s.iloc[:mid]
        current = s.iloc[mid:]
        psi_trigger_rate = population_stability_index(
            baseline, current, bins=10, min_samples=50
        )
    else:
        psi_trigger_rate = 0.0  # 데이터가 너무 적을 때는 변화 감지 무효

    # C-axis: Semantic Density metrics
    try:
        # Select numeric features (exclude target and timestamp-like)
        num_df = df.select_dtypes(include=['int64', 'float64', 'float32'])
        drop_cols = []
        for c in num_df.columns:
            if c.lower().startswith('time') or c.lower().endswith('stamp'):
                drop_cols.append(c)
        if 'target' in num_df.columns:
            drop_cols.append('target')
        
        X = num_df.drop(columns=[c for c in drop_cols if c in num_df.columns]).values
        intra_density, sil_approx, k_used = compute_density_metrics(X)
    except Exception:
        intra_density, sil_approx, k_used = None, None, None

    return {
        "st_var_ratio": st_var_ratio,
        "seasonal_corr": seasonal_corr,
        "psi_trigger_rate": psi_trigger_rate,
        "sk_k_score": sk_k_score,
        "outlier_impact": outlier_impact,
        "dip_stat": None,  # TODO
        "intra_cluster_density": intra_density,  # C1: Semantic Density
        "silhouette_approx": sil_approx,        # C2: Silhouette Score
        "density_k": k_used                      # C3: Optimal k used
    }

if __name__ == "__main__":
    df = pd.read_csv("data/raw/sample.csv")
    metrics = compute_axes(df)
    with open("metrics/axes_run.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print("axes_run.json written") 