import pandas as pd
import argparse
import numpy as np
import os

def main(src: str, out: str):
    df = pd.read_csv(src)
    df_shift = df.copy()

    # 숫자형 컬럼만 후보
    num_cols = df_shift.select_dtypes(include=['int64','float64','float32']).columns.tolist()
    # target, time 등 제외
    drop_keys = {'target','timestamp','time','datetime'}
    target_col = None
    for c in df_shift.columns[::-1]:
        if c.lower() == 'target':
            target_col = c
            break

    feature_cols = [c for c in num_cols if c.lower() not in drop_keys]
    if not feature_cols:
        raise ValueError("No numeric feature columns found to shift.")

    rng = np.random.default_rng(42)

    # 간단한 변환 규칙
    for i, col in enumerate(feature_cols):
        series = df_shift[col].astype(float)
        if i % 3 == 0:
            df_shift[col] = series + 0.8  # mean shift
        elif i % 3 == 1:
            df_shift[col] = series * 1.15  # scale
        else:
            df_shift[col] = series + rng.normal(0, series.std()*0.2, size=len(series))  # noise

    os.makedirs(os.path.dirname(out), exist_ok=True)
    df_shift.to_csv(out, index=False)
    print(f"Shifted dataset written to {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/raw/sample.csv")
    ap.add_argument("--out", default="data/raw/sample_shifted.csv")
    args = ap.parse_args()
    main(args.src, args.out) 