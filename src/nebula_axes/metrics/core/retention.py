import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from typing import Dict, Any, Optional

def _macro_f1(X, y):
    if y.nunique() <= 1:
        return None, None
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=42,
        stratify=y if y.nunique() > 1 else None
    )
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    f1 = f1_score(yte, pred, average="macro")
    return clf, f1

def _zero_shot(clf, X, y):
    if clf is None or y.nunique() <= 1:
        return None
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=42,
        stratify=y if y.nunique()>1 else None
    )
    pred = clf.predict(Xte)
    return f1_score(yte, pred, average="macro")

def _retrain(X, y):
    return _macro_f1(X, y)[1]

def compute_retention_metrics(df_base: pd.DataFrame,
                              df_shift: pd.DataFrame,
                              *,
                              min_samples=200):
    if len(df_base) < min_samples or len(df_shift) < min_samples:
        return {
            "macro_f1_base": None,
            "macro_f1_shifted_zero_shot": None,
            "macro_f1_shifted_retrained": None,
            "retention_zero_shot": None,
            "retention_retrained": None
        }
    target_col = df_base.columns[-1]
    Xb = df_base.drop(columns=[target_col]).select_dtypes(include=[np.number])
    yb = df_base[target_col]
    Xs = df_shift.drop(columns=[target_col]).select_dtypes(include=[np.number])
    ys = df_shift[target_col]

    clf, f1_base = _macro_f1(Xb, yb)
    f1_zero = _zero_shot(clf, Xs, ys)
    f1_re = _retrain(Xs, ys)

    retention_zero = (f1_zero / (f1_base + 1e-9)) if (f1_base and f1_zero) else None
    retention_re = (f1_re / (f1_base + 1e-9)) if (f1_base and f1_re) else None
    return {
        "macro_f1_base": f1_base,
        "macro_f1_shifted_zero_shot": f1_zero,
        "macro_f1_shifted_retrained": f1_re,
        "retention_zero_shot": retention_zero,
        "retention_retrained": retention_re
    } 