import pandas as pd, json, hashlib, time, argparse
from pathlib import Path

def ingest_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def profile(df: pd.DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "null_pct": df.isna().mean().round(4).to_dict(),
        "numeric_desc": df.describe(include='number').round(4).to_dict(),
        "hash_head100": hashlib.md5(str(df.head(100).to_dict()).encode()).hexdigest()
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_profile", default="metrics/dataset_profile.json")
    args = ap.parse_args()
    df = ingest_csv(args.input)
    prof = {"generated_at": time.time(), **profile(df)}
    Path(args.out_profile).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_profile, "w", encoding="utf-8") as f:
        json.dump(prof, f, indent=2)
    print("PROFILE_SAVED", args.out_profile)

if __name__ == "__main__":
    main() 