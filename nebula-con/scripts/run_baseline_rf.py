import argparse
import json

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


def main(data_path: str):
    df = pd.read_csv(data_path)
    # numeric features만 (timestamp 제외)
    df_num = df.select_dtypes(include=[np.number])
    # target은 마지막 컬럼 가정
    target = df.iloc[:, -1]
    X = df_num.iloc[:, :-1]
    y = target
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    )
    clf.fit(Xtr, ytr)
    preds = clf.predict(Xte)
    macro_f1 = f1_score(yte, preds, average="macro")
    result = {
        "macro_f1": macro_f1,
        "rows": len(df),
        "classes": int(y.nunique())
    }
    with open("metrics/baseline_run.json", "w") as f:
        json.dump(result, f, indent=2)
    print("BASELINE_DONE", result)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    args = ap.parse_args()
    main(args.data)
