import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def compute_density_metrics(df: pd.DataFrame,
                            *,
                            k_range=range(2,6),
                            min_samples=40,
                            random_state=42):
    # numeric feature subset
    num_df = df.select_dtypes(include=["float32","float64","int32","int64"]).copy()
    # Drop known non-feature columns
    for c in list(num_df.columns):
        cl = c.lower()
        if cl in ("target",) or cl.startswith("time") or cl.endswith("stamp"):
            num_df.drop(columns=[c], inplace=True, errors="ignore")
    if num_df.shape[1] < 2 or num_df.shape[0] < min_samples:
        return {
            "intra_cluster_density": None,
            "silhouette_approx": None,
            "density_k": None
        }
    X = num_df.dropna().values
    if X.shape[0] < min_samples:
        return {
            "intra_cluster_density": None,
            "silhouette_approx": None,
            "density_k": None
        }

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    best_score = -1
    best_k = None
    best_intra = None
    best_inter = None

    global_center = Xs.mean(axis=0)
    global_mean_center_dist = np.mean(np.linalg.norm(Xs - global_center, axis=1))
    global_ref = 2 * global_mean_center_dist

    for k in k_range:
        try:
            km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
            labels = km.fit_predict(Xs)
            centers = km.cluster_centers_
        except Exception:
            continue
        dist_to_center = np.linalg.norm(Xs - centers[labels], axis=1)
        intra = 2 * np.mean(dist_to_center)
        inter_dists = []
        for i in range(k):
            for j in range(i+1, k):
                inter_dists.append(np.linalg.norm(centers[i]-centers[j]))
        inter = np.mean(inter_dists) if inter_dists else None
        if inter and inter > intra and inter > 1e-9:
            sil_approx = (inter - intra)/(inter + 1e-9)
        else:
            sil_approx = 0.0
        if sil_approx > best_score:
            best_score = sil_approx
            best_k = k
            best_intra = intra
            best_inter = inter

    if best_k is None:
        return {
            "intra_cluster_density": None,
            "silhouette_approx": None,
            "density_k": None
        }
    intra_density = best_intra / (global_ref + 1e-9)
    return {
        "intra_cluster_density": float(intra_density),
        "silhouette_approx": float(best_score),
        "density_k": int(best_k)
    } 