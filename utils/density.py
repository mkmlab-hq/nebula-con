import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def compute_density_metrics(X: np.ndarray,
                            k_range=range(2,6),
                            min_samples=40,
                            random_state=42):
    """
    Compute semantic density metrics for clustering analysis.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        k_range: Range of k values to test for KMeans
        min_samples: Minimum samples required
        random_state: Random seed for reproducibility
        
    Returns:
        tuple: (intra_cluster_density, silhouette_approx, k_used)
    """
    if X is None or len(X.shape) != 2:
        return None, None, None
    n, d = X.shape
    if n < min_samples or d < 2:
        return None, None, None

    # Remove NaN rows
    mask = ~np.isnan(X).any(axis=1)
    Xc = X[mask]
    if len(Xc) < min_samples:
        return None, None, None

    # Standardize features
    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xc)

    best_score = -1
    best_k = None
    best_intra = None
    best_inter = None

    # Precompute global distance reference
    global_center = Xs.mean(axis=0)
    global_mean_center_dist = np.mean(np.linalg.norm(Xs - global_center, axis=1))
    global_ref = 2 * global_mean_center_dist  # pairwise distance approximation

    # Test different k values
    for k in k_range:
        try:
            km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
            labels = km.fit_predict(Xs)
            centers = km.cluster_centers_
        except Exception:
            continue

        # Intra-cluster distance (point to center, then 2x for pairwise approximation)
        dist_to_center = np.linalg.norm(Xs - centers[labels], axis=1)
        intra = 2 * np.mean(dist_to_center)

        # Inter-cluster distance (center to center)
        if k > 1:
            dists = []
            for i in range(k):
                for j in range(i+1, k):
                    dists.append(np.linalg.norm(centers[i] - centers[j]))
            inter = np.mean(dists) if dists else None
        else:
            inter = None

        # Silhouette approximation
        if inter is not None and inter > 1e-9 and inter > intra:
            sil_approx = (inter - intra) / (inter + 1e-9)
        else:
            sil_approx = 0.0

        # Selection criterion: maximize silhouette approximation
        if sil_approx > best_score:
            best_score = sil_approx
            best_k = k
            best_intra = intra
            best_inter = inter

    if best_k is None or best_intra is None:
        return None, None, None

    # Normalize intra-cluster density by global reference
    intra_density = best_intra / (global_ref + 1e-9)
    
    return float(intra_density), float(best_score), int(best_k) 