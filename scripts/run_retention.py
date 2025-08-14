import argparse
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from scipy.stats import ks_2samp

def load_dataset(path: str):
    df = pd.read_csv(path)
    return df

def select_xy(df: pd.DataFrame):
    # target: 마지막 열로 가정
    target_col = df.columns[-1]
    y = df[target_col]
    X = df.drop(columns=[target_col])
    # 숫자형만
    X = X.select_dtypes(include=[np.number])
    return X, y

def macro_f1_model(X, y):
    if y.nunique() <= 1:
        return None, None
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if y.nunique()>1 else None
    )
    clf = RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    )
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    f1 = f1_score(yte, pred, average="macro")
    return clf, f1

def evaluate_zero_shot(clf, X_shift, y_shift):
    if clf is None or y_shift.nunique() <= 1:
        return None
    # same split pattern for shifted
    Xtr, Xte, ytr, yte = train_test_split(
        X_shift, y_shift, test_size=0.25, random_state=42,
        stratify=y_shift if y_shift.nunique()>1 else None
    )
    pred = clf.predict(Xte)
    f1 = f1_score(yte, pred, average="macro")
    return f1

def retrain_shifted(X_shift, y_shift):
    return macro_f1_model(X_shift, y_shift)[1]

def feature_shift_intensity(df_base: pd.DataFrame, df_shift: pd.DataFrame, top_k=5):
    num_cols = set(df_base.select_dtypes(include=[np.number]).columns) & set(df_shift.columns)
    shifts = []
    for c in num_cols:
        try:
            base = df_base[c].dropna().values
            sh = df_shift[c].dropna().values
            if len(base) > 30 and len(sh) > 30:
                # KS distance as shift
                ks_stat = ks_2samp(base, sh, alternative='two-sided').statistic
            else:
                ks_stat = 0.0
            mean_diff = float(np.mean(sh) - np.mean(base))
            shifts.append((c, ks_stat, mean_diff))
        except Exception:
            continue
    shifts.sort(key=lambda x: x[1], reverse=True)
    return [
        {"feature": f, "ks_stat": ks, "mean_diff": md}
        for f, ks, md in shifts[:top_k]
    ]

def main(base_path: str, shifted_path: str, out_path: str):
    result = {}
    df_base = load_dataset(base_path)
    df_shift = load_dataset(shifted_path)

    Xb, yb = select_xy(df_base)
    Xs, ys = select_xy(df_shift)

    if len(df_base) < 200 or len(df_shift) < 200:
        result.update({
            "macro_f1_base": None,
            "macro_f1_shifted_zero_shot": None,
            "macro_f1_shifted_retrained": None,
            "retention_zero_shot": None,
            "retention_retrained": None,
            "shift_intensity_features": None,
            "dataset_shift_type": "synthetic_mean_scale",
            "note": "Insufficient samples"
        })
    else:
        clf, f1_base = macro_f1_model(Xb, yb)
        f1_zero = evaluate_zero_shot(clf, Xs, ys)
        f1_retrain = retrain_shifted(Xs, ys)

        retention_zero = (f1_zero / (f1_base + 1e-9)) if (f1_zero is not None and f1_base) else None
        retention_re = (f1_retrain / (f1_base + 1e-9)) if (f1_retrain is not None and f1_base) else None

        shift_feats = feature_shift_intensity(df_base, df_shift)
        result.update({
            "macro_f1_base": f1_base,
            "macro_f1_shifted_zero_shot": f1_zero,
            "macro_f1_shifted_retrained": f1_retrain,
            "retention_zero_shot": retention_zero,
            "retention_retrained": retention_re,
            "shift_intensity_features": shift_feats,
            "dataset_shift_type": "synthetic_mean_scale"
        })

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Retention metrics written to {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="data/raw/sample.csv")
    ap.add_argument("--shifted", default="data/raw/sample_shifted.csv")
    ap.add_argument("--out", default="metrics/retention_run.json")
    args = ap.parse_args()
    main(args.base, args.shifted, args.out) 