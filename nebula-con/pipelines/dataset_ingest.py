import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# axes 모듈이 sys.path에 추가되어야 임포트 가능
sys.path.append('.')
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from axes.feature_builder import compute_axes  # axes 모듈에서 compute_axes 임포트
from utils.dip import approximate_dip


def ingest_csv(path: str) -> pd.DataFrame:
    """CSV 파일을 읽어 DataFrame으로 반환합니다."""
    return pd.read_csv(path)


def profile(df: pd.DataFrame) -> dict:
    """DataFrame의 기본 통계 프로파일을 생성합니다."""
    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "null_pct": df.isna().mean().round(4).to_dict(),
        "numeric_desc": df.describe(include="number").round(4).to_dict(),
        "hash_head100": hashlib.md5(str(df.head(100).to_dict()).encode()).hexdigest(),
    }


def population_stability_index(expected, actual, bins=10, min_samples=50):
    """Calculate Population Stability Index (PSI) between two distributions."""
    expected = np.array(expected, dtype=float)
    actual = np.array(actual, dtype=float)

    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]

    if len(expected) < min_samples or len(actual) < min_samples:
        return 0.0

    if np.array_equal(expected, actual):
        return 0.0

    global_min = min(np.min(expected), np.min(actual))
    global_max = max(np.max(expected), np.max(actual))

    if global_min == global_max:
        return 0.0

    epsilon = 1e-10
    bin_edges = np.linspace(global_min - epsilon, global_max + epsilon, bins + 1)

    expected_hist, _ = np.histogram(expected, bins=bin_edges)
    actual_hist, _ = np.histogram(actual, bins=bin_edges)

    expected_hist = expected_hist.astype(float) + 1e-10
    actual_hist = actual_hist.astype(float) + 1e-10

    expected_p = expected_hist / np.sum(expected_hist)
    actual_p = actual_hist / np.sum(actual_hist)

    psi = 0.0
    for i in range(len(expected_p)):
        if expected_p[i] > 0 and actual_p[i] > 0:
            psi += (actual_p[i] - expected_p[i]) * np.log(actual_p[i] / expected_p[i])

    return float(psi)


def compute_density_metrics(
    X: np.ndarray, k_range=range(2, 6), min_samples=40, random_state=42
):
    """Compute semantic density metrics for clustering analysis."""
    if X is None or len(X.shape) != 2:
        return None, None, None
    n, d = X.shape
    if n < min_samples or d < 2:
        return None, None, None

    mask = ~np.isnan(X).any(axis=1)
    Xc = X[mask]
    if len(Xc) < min_samples:
        return None, None, None

    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xc)

    best_score = -1
    best_k = None
    best_intra = None
    # best_inter = None  # 미사용 변수

    global_center = Xs.mean(axis=0)
    global_mean_center_dist = np.mean(np.linalg.norm(Xs - global_center, axis=1))
    global_ref = 2 * global_mean_center_dist

    for k in k_range:
        try:
            km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
            labels = km.fit_predict(Xs)
            centers = km.cluster_centers_
        except Exception:
            continue

        dist_to_center = np.linalg.norm(Xs - centers[labels], axis=1)
        intra = 2 * np.mean(dist_to_center)

        if k > 1:
            dists = []
            for i in range(k):
                for j in range(i + 1, k):
                    dists.append(np.linalg.norm(centers[i] - centers[j]))
            inter = np.mean(dists) if dists else None
        else:
            inter = None

        if inter is not None and inter > 1e-9 and inter > intra:
            sil_approx = (inter - intra) / (inter + 1e-9)
        else:
            sil_approx = 0.0

        if sil_approx > best_score:
            best_score = sil_approx
            best_k = k
            best_intra = intra
            # best_inter = inter  # 미사용 변수

    if best_k is None or best_intra is None:
        return None, None, None

    intra_density = best_intra / (global_ref + 1e-9)

    return float(intra_density), float(best_score), int(best_k)


def compute_axes(df: pd.DataFrame) -> dict:
    """Compute all 4 axes metrics (A/B/C/D)."""
    # Handle timestamp and target columns
    time_col = df.columns[0]  # First column as timestamp
    target_col = df.columns[-1]  # Last column as target

    # Convert timestamp if needed
    if df[time_col].dtype == "O":
        try:
            df[time_col] = pd.to_datetime(df[time_col])
        except Exception:
            pass

    # Convert target to numeric if possible
    if df[target_col].dtype == "O":
        try:
            df[target_col] = pd.Categorical(df[target_col]).codes
        except Exception:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]

    s = df.sort_values(time_col)[target_col].astype(float)

    # A-axis: Temporal Stability
    if len(s) < 30:
        st_var_ratio = np.nan
        seasonal_corr = np.nan
        psi_trigger_rate = np.nan
    else:
        global_var = float(s.var())
        win = min(24, max(5, len(s) // 10))
        roll_var = float(s.rolling(window=win, min_periods=5).var().mean())
        st_var_ratio = roll_var / (global_var + 1e-9)
        lag = min(24, max(2, len(s) // 12))
        seasonal_corr = s.autocorr(lag=lag)

        # A3: PSI calculation
        n = len(s)
        if n >= 120:
            mid = n // 2
            baseline = s.iloc[:mid]
            current = s.iloc[mid:]
            psi_trigger_rate = population_stability_index(
                baseline, current, bins=10, min_samples=50
            )
        else:
            psi_trigger_rate = 0.0

    # B-axis: Distributional Shape
    s_clean = s.astype(float).dropna()
    skew = s_clean.skew()
    kurt = s_clean.kurtosis()
    sk_k_score = float(abs(skew) + abs(kurt - 3))
    q1, q3 = s_clean.quantile(0.25), s_clean.quantile(0.75)
    iqr = (q3 - q1) + 1e-9
    outlier_ratio = float(
        ((s_clean < q1 - 1.5 * iqr) | (s_clean > q3 + 1.5 * iqr)).mean()
    )
    dip_stat = approximate_dip(s_clean.values)  # Hartigan dip test implemented

    # C-axis: Semantic Density
    try:
        num_df = df.select_dtypes(include=["int64", "float64", "float32"])
        drop_cols = []
        for c in num_df.columns:
            if c.lower().startswith("time") or c.lower().endswith("stamp"):
                drop_cols.append(c)
        if target_col in num_df.columns:
            drop_cols.append(target_col)

        X = num_df.drop(columns=[c for c in drop_cols if c in num_df.columns]).values
        intra_density, sil_approx, k_used = compute_density_metrics(X)
    except Exception:
        intra_density, sil_approx, k_used = None, None, None

    return {
        "st_var_ratio": st_var_ratio,
        "seasonal_corr": (
            float(seasonal_corr) if seasonal_corr is not None else np.nan
        ),
        "psi_trigger_rate": psi_trigger_rate,
        "sk_k_score": sk_k_score,
        "outlier_ratio": outlier_ratio,
        "dip_stat": dip_stat,
        "intra_cluster_density": intra_density,
        "silhouette_approx": sil_approx,
        "density_k": k_used,
    }


def main():
    """데이터셋을 수집하고 프로파일 및 axes 지표를 생성합니다."""
    ap = argparse.ArgumentParser(description="Ingest CSV data and generate dataset profile and axes metrics.")
    ap.add_argument("--input", required=True, help="Input CSV file path.")
    ap.add_argument("--out_profile", default="metrics/dataset_profile.json", help="Output path for dataset profile JSON.")
    ap.add_argument("--out_axes", default="metrics/axes_metrics.json", help="Output path for axes metrics JSON.")
    args = ap.parse_args()

    print(f"🚀 데이터 수집 시작: {args.input}")
    df = ingest_csv(args.input)
    print(f"✅ 데이터 로딩 완료. {len(df)} 행, {df.shape[1]} 열.")

    # 1. 데이터 프로파일 생성 및 저장
    prof = {"generated_at": time.time(), **profile(df)}
    Path(args.out_profile).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_profile, "w", encoding="utf-8") as f:
        json.dump(prof, f, indent=2)
    print(f"✅ 데이터 프로파일 저장 완료: {args.out_profile}")

    # 2. Axes 지표 생성 및 저장
    print("🧠 Axes 지표 계산 시작...")
    axes_metrics = compute_axes(df)
    axes_output = {"generated_at": time.time(), **axes_metrics}
    Path(args.out_axes).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_axes, "w", encoding="utf-8") as f:
        json.dump(axes_output, f, indent=2)
    print(f"✅ Axes 지표 저장 완료: {args.out_axes}")

    print("🎉 데이터 수집 및 분석 파이프라인 완료!")


if __name__ == "__main__":
    main()
