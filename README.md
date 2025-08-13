# NebulaCon - 캐글 BigQuery AI 해커톤 메인 작업 공간 🏆

## 🎯 프로젝트 개요
**NebulaCon은 MKM Lab의 캐글 BigQuery AI 해커톤 1위 달성을 위한 공식 메인 작업 공간입니다.**

### Mission
Cross-dataset generalization & drift robustness lens (Kaggle/CPGP Tier0Tier3)

## 🏗️ 핵심 구성 요소

### Tier0 Exit (Must):
- axes_registry.json v0.1 with 12 micro axes
- Working ingest profile JSON
- Baseline macro_f1 logged (metrics/baseline_run.json)
- Axes feature dump (stdout or metrics/axes_sample.json)
- CI green (lint+baseline smoke)

## 📁 프로젝트 구조
```
nebula-con/
├── src/                    # 소스 코드
├── data/                   # 데이터 파일
├── models/                 # 훈련된 모델
├── notebooks/              # Jupyter 노트북
├── tests/                  # 테스트 코드
├── .github/                # CI/CD 워크플로우
├── docs/                   # 프로젝트 문서
└── README.md               # 이 파일
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 실제 값 설정
```

### 2. 개발 서버 실행
```bash
# 개발 모드로 실행
python main.py

# 또는 Jupyter 노트북 실행
jupyter notebook
```

### 3. 테스트 실행
```bash
# 전체 테스트 실행
pytest

# 특정 테스트 실행
pytest tests/test_specific.py
```

