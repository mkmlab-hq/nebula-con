import pandas as pd
import json
import hashlib
import time
import argparse
from pathlib import Path
import sys

# axes 모듈이 sys.path에 추가되어야 임포트 가능
sys.path.append('.')
from axes.feature_builder import compute_axes # axes 모듈에서 compute_axes 임포트

def ingest_csv(path: str) -> pd.DataFrame:
    """CSV 파일을 읽어 DataFrame으로 반환합니다."""
    return pd.read_csv(path)

def profile(df: pd.DataFrame) -> dict:
    """DataFrame의 기본 통계 프로파일을 생성합니다."""
    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "null_pct": df.isna().mean().round(4).to_dict(),
        "numeric_desc": df.describe(include='number').round(4).to_dict(),
        "hash_head100": hashlib.md5(str(df.head(100).to_dict()).encode()).hexdigest()
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
