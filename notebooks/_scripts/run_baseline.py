import pandas as pd, json, time, argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="metrics/baseline_run.json")
    args = ap.parse_args()
    df = pd.read_csv(args.data)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    stratify = y if y.nunique() < 50 else None
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=stratify)
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(Xtr, ytr)
    preds = clf.predict(Xte)
    macro_f1 = f1_score(yte, preds, average="macro")
    out = {
        "timestamp": time.time(),
        "model": "RandomForestClassifier",
        "macro_f1": macro_f1,
        "rows": int(len(df)),
        "classes": int(y.nunique())
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print("BASELINE_DONE", out)

if __name__ == "__main__":
    main() 