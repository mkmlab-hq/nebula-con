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

## 🔄 CI/CD 파이프라인

### GitHub Actions 워크플로우
- **자동 테스트**: 코드 변경 시 자동 테스트 실행
- **품질 검사**: linting, formatting, security scan
- **모델 검증**: baseline 성능 자동 검증
- **배포**: 성공 시 자동 배포

### 워크플로우 파일
- `.github/workflows/ci.yml`: 메인 CI/CD 파이프라인

## 📊 성능 지표

### 현재 상태
- **Baseline F1**: [metrics/baseline_run.json에서 확인]
- **Axes 등록**: 12 micro axes 등록 완료
- **CI 상태**: [GitHub Actions에서 확인]

### 목표
- **캐글 대회 1위 달성** 🏆
- **Cross-dataset generalization** 향상
- **Drift robustness** 개선

## 🤝 기여 가이드라인

### 개발 규칙
1. **코드 품질**: PEP 8, type hints, docstrings 필수
2. **테스트**: 새로운 기능에는 반드시 테스트 작성
3. **문서**: 코드 변경 시 관련 문서 업데이트
4. **커밋**: 명확한 커밋 메시지 작성

### 브랜치 전략
- **main**: 안정적인 메인 브랜치
- **feature/**: 새로운 기능 개발
- **bugfix/**: 버그 수정
- **hotfix/**: 긴급 수정

## 📚 관련 문서

### 프로젝트 문서
- [프로젝트 구조](./docs/PROJECT_STRUCTURE.md)
- [API 문서](./docs/API.md)
- [모델 아키텍처](./docs/MODEL_ARCHITECTURE.md)

### 워크스페이스 문서
- [워크스페이스 규칙](../mkm-lab-workspace-config/WORKSPACE_RULES.md)
- [공통 설정](../mkm-lab-workspace-config/)

## 🔗 외부 링크

### 캐글 대회
- [BigQuery AI 해커톤 페이지](https://www.kaggle.com/competitions/bigquery-ai-hackathon)
- [대회 규칙 및 평가 기준]

### MKM Lab
- [중앙 AI 두뇌](../mkm-core-ai/) - AI 모듈 공급원
- [공통 설정](../mkm-lab-workspace-config/) - 개발 환경 설정

## 📞 지원

### 이슈 및 문의
- **기능 요청**: GitHub Issues에 Feature Request 생성
- **버그 리포트**: GitHub Issues에 Bug Report 생성
- **일반 문의**: GitHub Discussions 활용

### 팀 멤버
- **프로젝트 리더**: [이름]
- **AI 모델 담당**: [이름]
- **데이터 엔지니어**: [이름]
- **DevOps 담당**: [이름]

---

**🏆 캐글 BigQuery AI 해커톤 1위 달성을 위해 함께 노력합시다!**

**💡 팁: 모든 캐글 해커톤 관련 작업은 이 `nebula-con` 레포지토리에서 진행하세요!**
