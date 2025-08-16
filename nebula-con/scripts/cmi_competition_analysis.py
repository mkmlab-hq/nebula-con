#!/usr/bin/env python3
"""
CMI 대회 데이터 분석 스크립트
데이터 구조, 결측값, 센서 종류 등을 분석하여 모델 개발 전략 수립
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_cmi_dataset():
    """CMI 대회 데이터셋을 분석합니다."""
    
    print("🔍 CMI 대회 데이터셋 분석 시작...")
    
    # 데이터 파일 경로 확인
    data_files = [
        "train.csv",
        "train_demographics.csv", 
        "test.csv",
        "sample_submission.csv"
    ]
    
    print("\n📁 데이터 파일 존재 여부 확인:")
    for file in data_files:
        if Path(file).exists():
            print(f"✅ {file} - 존재")
        else:
            print(f"❌ {file} - 없음")
    
    # train.csv 분석
    if Path("train.csv").exists():
        print("\n🔍 train.csv 구조 분석:")
        try:
            train_df = pd.read_csv("train.csv")
            print(f"✅ 데이터 로드 성공")
            print(f"📊 데이터 크기: {train_df.shape}")
            print(f"📋 컬럼 목록: {list(train_df.columns)}")
            
            # 기본 통계
            print(f"\n📈 기본 통계:")
            print(f"  - 메모리 사용량: {train_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            print(f"  - 결측값: {train_df.isnull().sum().sum()}")
            
            # 데이터 타입 분석
            print(f"\n🔧 데이터 타입:")
            print(train_df.dtypes.value_counts())
            
            # 첫 번째 행 샘플
            print(f"\n📝 첫 번째 행 샘플:")
            print(train_df.head(1).to_string())
            
        except Exception as e:
            print(f"❌ train.csv 분석 실패: {str(e)}")
    
    # train_demographics.csv 분석
    if Path("train_demographics.csv").exists():
        print("\n🔍 train_demographics.csv 구조 분석:")
        try:
            demo_df = pd.read_csv("train_demographics.csv")
            print(f"✅ 데이터 로드 성공")
            print(f"📊 데이터 크기: {demo_df.shape}")
            print(f"📋 컬럼 목록: {list(demo_df.columns)}")
            
            # 인구통계학적 정보
            print(f"\n👥 인구통계학적 정보:")
            for col in demo_df.columns:
                if demo_df[col].dtype == 'object':
                    print(f"  - {col}: {demo_df[col].value_counts().to_dict()}")
                else:
                    print(f"  - {col}: {demo_df[col].describe().to_dict()}")
                    
        except Exception as e:
            print(f"❌ train_demographics.csv 분석 실패: {str(e)}")
    
    # test.csv 분석
    if Path("test.csv").exists():
        print("\n🔍 test.csv 구조 분석:")
        try:
            test_df = pd.read_csv("test.csv")
            print(f"✅ 데이터 로드 성공")
            print(f"📊 데이터 크기: {test_df.shape}")
            print(f"📋 컬럼 목록: {list(test_df.columns)}")
            
            # train과 test 비교
            if Path("train.csv").exists():
                train_df = pd.read_csv("train.csv")
                print(f"\n🔄 Train vs Test 비교:")
                print(f"  - Train 컬럼 수: {len(train_df.columns)}")
                print(f"  - Test 컬럼 수: {len(test_df.columns)}")
                print(f"  - 공통 컬럼: {len(set(train_df.columns) & set(test_df.columns))}")
                
        except Exception as e:
            print(f"❌ test.csv 분석 실패: {str(e)}")
    
    # sample_submission.csv 분석
    if Path("sample_submission.csv").exists():
        print("\n🔍 sample_submission.csv 구조 분석:")
        try:
            sub_df = pd.read_csv("sample_submission.csv")
            print(f"✅ 데이터 로드 성공")
            print(f"📊 데이터 크기: {sub_df.shape}")
            print(f"📋 컬럼 목록: {list(sub_df.columns)}")
            
            # 제출 형식 확인
            print(f"\n📤 제출 형식:")
            print(f"  - 제출해야 할 행 수: {len(sub_df)}")
            print(f"  - 예측해야 할 컬럼: {list(sub_df.columns)}")
            
        except Exception as e:
            print(f"❌ sample_submission.csv 분석 실패: {str(e)}")


def suggest_model_strategy():
    """데이터 분석 결과를 바탕으로 모델 개발 전략을 제시합니다."""
    
    print("\n🚨 모델 개발 전략 제시...")
    
    print("\n1️⃣ 데이터 전처리 전략:")
    print("   - 센서 데이터 정규화 및 스케일링")
    print("   - 결측값 처리 (보간, 평균값 대체)")
    print("   - 시계열 데이터 윈도우링")
    print("   - 피처 엔지니어링 (통계적 특성 추출)")
    
    print("\n2️⃣ 모델 아키텍처 전략:")
    print("   - 전통적 ML: Random Forest, XGBoost")
    print("   - 딥러닝: LSTM, 1D CNN")
    print("   - 앙상블: 여러 모델 조합")
    
    print("\n3️⃣ 평가 및 최적화 전략:")
    print("   - 교차 검증 (시계열 데이터 고려)")
    print("   - 하이퍼파라미터 튜닝")
    print("   - 앙상블 가중치 최적화")


def main():
    """메인 실행 함수"""
    print("🚨 CMI 대회 데이터셋 분석 시작...")
    
    try:
        analyze_cmi_dataset()
        suggest_model_strategy()
        print("\n✅ CMI 대회 데이터셋 분석 완료!")
        
    except Exception as e:
        print(f"❌ 분석 실패: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 