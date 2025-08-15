import argparse
import json
import time

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--shifted_data", default=None)
    ap.add_argument("--out", default="data/baseline_run.json")
    ap.add_argument("--out_retention", default="data/retention_metrics.json")
    args = ap.parse_args()

    df = pd.read_csv(args.data)
    # Separate features/target
    X_all = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Convert target to numeric if needed while keeping it a Series
    if y.dtype == "O":
        try:
            y = pd.Series(pd.Categorical(y).codes, index=y.index)
        except Exception:
            pass

    # Use only numeric feature columns (drop timestamp/object/datetime)
    X = X_all.select_dtypes(include=[np.number])

    stratify = y if y.nunique() < 50 else None
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(Xtr, ytr)
    preds = clf.predict(Xte)
    macro_f1 = f1_score(yte, preds, average="macro")

    out = {
        "timestamp": time.time(),
        "model": "RandomForestClassifier",
        "macro_f1": macro_f1,
        "rows": int(len(df)),
        "classes": int(y.nunique()),
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print("BASELINE_DONE", out)

    # Retention metrics if shifted data provided
    if args.shifted_data:
        try:
            df_shift = pd.read_csv(args.shifted_data)
            X_shift_all = df_shift.iloc[:, :-1]
            y_shift = df_shift.iloc[:, -1]

            if y_shift.dtype == "O":
                try:
                    y_shift = pd.Series(
                        pd.Categorical(y_shift).codes, index=y_shift.index
                    )
                except Exception:
                    pass

            # Use only numeric columns for shifted dataset as well
            X_shift = X_shift_all.select_dtypes(include=[np.number])

            # Zero-shot evaluation
            Xtr_shift, Xte_shift, ytr_shift, yte_shift = train_test_split(
                X_shift,
                y_shift,
                test_size=0.2,
                random_state=42,
                stratify=y_shift if y_shift.nunique() < 50 else None,
            )

            # Evaluate original model on shifted data
            preds_zero = clf.predict(Xte_shift)
            f1_zero_shot = f1_score(yte_shift, preds_zero, average="macro")

            # Retrain on shifted data
            clf_shift = RandomForestClassifier(
                n_estimators=200, random_state=42, n_jobs=-1
            )
            clf_shift.fit(Xtr_shift, ytr_shift)
            preds_retrain = clf_shift.predict(Xte_shift)
            f1_retrained = f1_score(yte_shift, preds_retrain, average="macro")

            # Calculate retention ratios
            retention_zero = f1_zero_shot / (macro_f1 + 1e-9)
            retention_retrained = f1_retrained / (macro_f1 + 1e-9)

            # Feature shift intensity computed on numeric feature intersection
            shift_intensity = []
            common_cols = [c for c in X.columns if c in X_shift.columns]
            for col in common_cols:
                try:
                    base_vals = X[col].dropna().values
                    shift_vals = X_shift[col].dropna().values
                    if len(base_vals) > 30 and len(shift_vals) > 30:
                        ks_stat = ks_2samp(base_vals, shift_vals).statistic
                        mean_diff = float(np.mean(shift_vals) - np.mean(base_vals))
                        shift_intensity.append(
                            {
                                "feature": col,
                                "ks_stat": float(ks_stat),
                                "mean_diff": mean_diff,
                            }
                        )
                except Exception:
                    continue

            shift_intensity.sort(key=lambda x: x["ks_stat"], reverse=True)

            retention_out = {
                "macro_f1_base": macro_f1,
                "macro_f1_shifted_zero_shot": f1_zero_shot,
                "macro_f1_shifted_retrained": f1_retrained,
                "retention_zero_shot": retention_zero,
                "retention_retrained": retention_retrained,
                "shift_intensity_features": shift_intensity[:5],
                "dataset_shift_type": "synthetic_mean_scale",
            }

            with open(args.out_retention, "w") as f:
                json.dump(retention_out, f, indent=2)
            print("RETENTION_DONE", retention_out)

        except Exception as e:
            print(f"Retention calculation failed: {e}")


if __name__ == "__main__":
    main()
