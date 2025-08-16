# 🔄 MKM Lab 작업 워크플로우 가이드 (v3.0)

## 📋 문서 정보
- **제목**: MKM Lab 작업 워크플로우 가이드
- **버전**: 3.0 (GitHub 생태계 전환)
- **작성일**: 2024년 12월
- **작성자**: MKM Lab DevOps팀
- **승인자**: 프로젝트 총책임자

## 🎯 개요

### **GitHub 생태계 전환의 의미**
MKM Lab은 2024년 12월, 모든 개발 및 연구 프로세스를 **GitHub 중심 생태계**로 전환했습니다. 이는 단순한 도구 변경이 아닌, **작업 방식의 근본적 혁신**을 의미합니다.

### **핵심 철학**
```
🔄 새로운 작업 패러다임
├── GitHub: 모든 작업의 중심 허브
├── 자동화: GitHub Actions를 통한 프로세스 자동화
├── 협업: 실시간 협업 및 코드 리뷰
└── 품질: 자동화된 테스트 및 배포
```

## 🏗️ 개발 환경 설정

### **1. 중앙 워크스페이스 구성**
```bash
# 1. 중앙 워크스페이스 생성
mkdir F:\workspace
cd F:\workspace

# 2. 모든 프로젝트 클론
git clone https://github.com/mkmlab-hq/mkm-analysis-engine.git
git clone https://github.com/mkmlab-hq/persona-diary-frontend.git
git clone https://github.com/mkmlab-hq/chart-assistant.git
git clone https://github.com/mkmlab-hq/mkm-inst-web.git
git clone https://github.com/mkmlab-hq/mkm-med-platform.git

# 3. 환경 변수 설정
cp mkm-analysis-engine/env.example mkm-analysis-engine/.env
# .env 파일에 실제 API 키 입력
```

### **2. GitHub Secrets 설정**
각 레포지토리의 Settings > Secrets and variables > Actions에서 설정:

**필수 Secrets:**
```yaml
# API Keys
OPENAI_API_KEY: "sk-..."
GOOGLE_AI_API_KEY: "AIza..."
GEMINI_API_KEY: "AIza..."
TELEGRAM_BOT_TOKEN: "1234567890:ABC..."
MKM_API_KEY: "mkm_..."

# GCS Settings
ENABLE_GCS_UPLOAD: "true"
GCS_BUCKET_NAME: "mkm-knowledge-base-bucket"
GCP_PROJECT_ID: "persona-diary-service"

# Database
DATABASE_URL: "postgresql://..."
JWT_SECRET_KEY: "your-secret-key"

# Environment
NODE_ENV: "production"
PYTHON_ENV: "production"
LOG_LEVEL: "INFO"
```

## 🔄 일일 작업 워크플로우

### **1. 작업 시작**
```bash
# 1. 최신 코드 동기화
cd F:\workspace\mkm-analysis-engine
git pull origin main

# 2. 브랜치 생성 (새 기능 개발 시)
git checkout -b feature/new-feature-name

# 3. 환경 확인
python -c "import os; print('Environment loaded:', bool(os.getenv('OPENAI_API_KEY')))"
```

### **2. 개발 작업**
```bash
# 1. 코드 수정 및 개발
# - IDE에서 코드 편집
# - 로컬 테스트 실행

# 2. 변경사항 확인
git status
git diff

# 3. 변경사항 스테이징
git add .
git commit -m "FEAT: 새로운 기능 추가

- 구체적인 변경사항 설명
- 관련 이슈 번호: #123"
```

### **3. 품질 검증**
```bash
# 1. 로컬 테스트 실행
python -m pytest tests/
python -m flake8 src/
python -m mypy src/

# 2. 환경 변수 검증
python test_env_values.py

# 3. API 테스트
python api_validation_test.py
```

### **4. 코드 푸시 및 리뷰**
```bash
# 1. 원격 저장소에 푸시
git push origin feature/new-feature-name

# 2. GitHub에서 Pull Request 생성
# - 제목: "FEAT: 새로운 기능 추가"
# - 설명: 변경사항 상세 설명
# - 리뷰어 지정

# 3. 코드 리뷰 및 승인
# - 팀원과 코드 리뷰
# - 피드백 반영
# - 승인 후 main 브랜치로 머지
```

## 🤖 자동화 워크플로우

### **1. GitHub Actions 파이프라인**
```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python -m pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: echo "Deploy to production"
```

### **2. 데이터 수집 자동화**
```yaml
# .github/workflows/data-collection.yml
name: Data Collection
on:
  schedule:
    - cron: '0 */6 * * *'  # 6시간마다
  workflow_dispatch:

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - name: Collect data
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ENABLE_GCS_UPLOAD: ${{ secrets.ENABLE_GCS_UPLOAD }}
        run: python collectors/ai_researcher_collector.py
```

## 📊 데이터 관리 워크플로우

### **1. 데이터 수집**
```python
# collectors/ai_researcher_collector.py
import os
from google.cloud import storage

def save_data(data, filename):
    """데이터를 로컬과 GCS에 저장"""
    
    # 1. 로컬 저장 (항상)
    data.to_csv(f"data/{filename}", index=False)
    
    # 2. GCS 업로드 (조건부)
    gcs_enabled = os.getenv('ENABLE_GCS_UPLOAD', 'false').lower() == 'true'
    if gcs_enabled:
        upload_to_gcs(f"data/{filename}", filename)

def upload_to_gcs(local_path, gcs_path):
    """GCS에 파일 업로드"""
    client = storage.Client()
    bucket = client.bucket(os.getenv('GCS_BUCKET_NAME'))
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
```

### **2. 데이터 품질 관리**
```python
# scripts/data_quality_check.py
def validate_data_quality():
    """데이터 품질 검증"""
    
    # 1. 허위 데이터 제거
    remove_fake_data()
    
    # 2. 중복 데이터 검사
    remove_duplicates()
    
    # 3. 데이터 검증
    validate_schema()
    
    # 4. 품질 보고서 생성
    generate_quality_report()
```

### **3. 데이터 동기화**
```python
# scripts/sync_gcs_to_github.py
def sync_data():
    """GCS에서 GitHub로 데이터 동기화"""
    
    # 1. GCS에서 데이터 다운로드
    download_from_gcs()
    
    # 2. 로컬에 저장
    save_locally()
    
    # 3. Git 커밋
    commit_changes()
    
    # 4. GitHub에 푸시
    push_to_github()
```

## 🔒 보안 워크플로우

### **1. API 키 관리**
```bash
# 1. 로컬 환경 변수 설정
cp env.example .env
# .env 파일에 실제 API 키 입력

# 2. GitHub Secrets 설정
# Settings > Secrets and variables > Actions
# 각 API 키를 개별 Secret으로 추가

# 3. 환경 변수 검증
python test_env_values.py
```

### **2. 코드 보안 검사**
```bash
# 1. 보안 취약점 스캔
pip install safety
safety check

# 2. 하드코딩된 키 검사
grep -r "sk-" src/
grep -r "AIza" src/

# 3. .gitignore 확인
cat .gitignore
```

### **3. 접근 권한 관리**
```bash
# 1. Git 사용자 설정
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 2. SSH 키 설정 (선택사항)
ssh-keygen -t ed25519 -C "your.email@example.com"
# GitHub에 공개키 추가
```

## 📈 모니터링 워크플로우

### **1. 성능 모니터링**
```python
# scripts/monitor_performance.py
def monitor_system():
    """시스템 성능 모니터링"""
    
    # 1. GitHub 저장소 크기 확인
    check_repo_size()
    
    # 2. GCS 사용량 확인
    check_gcs_usage()
    
    # 3. API 응답 시간 확인
    check_api_response_time()
    
    # 4. 오류율 확인
    check_error_rate()
```

### **2. 비용 모니터링**
```bash
# 1. GCS 비용 확인
gcloud billing accounts list
gcloud billing accounts describe ACCOUNT_ID

# 2. GitHub 사용량 확인
# GitHub Insights에서 확인

# 3. API 사용량 확인
# 각 API 제공업체 대시보드에서 확인
```

### **3. 품질 지표 모니터링**
```python
# scripts/quality_metrics.py
def track_quality_metrics():
    """품질 지표 추적"""
    
    metrics = {
        'code_coverage': get_test_coverage(),
        'data_accuracy': get_data_accuracy(),
        'system_uptime': get_system_uptime(),
        'user_satisfaction': get_user_satisfaction()
    }
    
    # 지표를 GitHub Issues나 외부 도구에 기록
    log_metrics(metrics)
```

## 🚀 배포 워크플로우

### **1. 스테이징 배포**
```yaml
# .github/workflows/staging.yml
name: Deploy to Staging
on:
  push:
    branches: [ develop ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment"
          # 스테이징 배포 스크립트
```

### **2. 프로덕션 배포**
```yaml
# .github/workflows/production.yml
name: Deploy to Production
on:
  push:
    branches: [ main ]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production environment"
          # 프로덕션 배포 스크립트
```

### **3. 롤백 절차**
```bash
# 1. 이전 버전으로 롤백
git revert HEAD

# 2. 롤백 커밋 푸시
git push origin main

# 3. 배포 확인
# GitHub Actions에서 배포 상태 확인
```

## 📚 문서화 워크플로우

### **1. 코드 문서화**
```python
def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    데이터를 처리하여 분석 가능한 형태로 변환합니다.
    
    Args:
        data (pd.DataFrame): 원본 데이터
        
    Returns:
        pd.DataFrame: 처리된 데이터
        
    Raises:
        ValueError: 데이터가 비어있는 경우
    """
    if data.empty:
        raise ValueError("데이터가 비어있습니다.")
    
    # 데이터 처리 로직
    processed_data = data.copy()
    # ... 처리 과정
    
    return processed_data
```

### **2. README 업데이트**
```markdown
# 프로젝트 제목

## 개요
프로젝트에 대한 간단한 설명

## 설치 방법
```bash
git clone https://github.com/mkmlab-hq/project-name.git
cd project-name
pip install -r requirements.txt
```

## 사용 방법
사용 예시 코드

## 기여 방법
기여 가이드라인

## 라이선스
라이선스 정보
```

### **3. API 문서화**
```python
# FastAPI를 사용한 API 문서화
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MKM Analysis API",
    description="AI 기반 체질 분석 API",
    version="3.0"
)

class AnalysisRequest(BaseModel):
    image_url: str
    analysis_type: str

@app.post("/analyze")
async def analyze_constitution(request: AnalysisRequest):
    """
    체질 분석을 수행합니다.
    
    - **image_url**: 분석할 이미지 URL
    - **analysis_type**: 분석 유형 (face, voice, tongue)
    """
    # 분석 로직
    return {"result": "analysis_result"}
```

## 🎯 성공 지표

### **개발 효율성**
- **코드 리뷰 시간**: 평균 24시간 이하
- **배포 빈도**: 주 3회 이상
- **버그 발견률**: 프로덕션 배포 후 1주일 내 5% 이하

### **품질 지표**
- **테스트 커버리지**: 80% 이상
- **코드 품질**: A등급 이상
- **보안 취약점**: 0건

### **운영 지표**
- **시스템 가용성**: 99.9% 이상
- **응답 시간**: 평균 2초 이하
- **사용자 만족도**: 4.5/5.0 이상

## 📋 체크리스트

### **일일 체크리스트**
- [ ] 최신 코드 동기화 (git pull)
- [ ] 환경 변수 확인
- [ ] 로컬 테스트 실행
- [ ] 변경사항 커밋 및 푸시
- [ ] GitHub Actions 상태 확인

### **주간 체크리스트**
- [ ] 코드 리뷰 참여
- [ ] 성능 지표 확인
- [ ] 보안 스캔 실행
- [ ] 문서 업데이트
- [ ] 팀 회의 참석

### **월간 체크리스트**
- [ ] 아키텍처 검토
- [ ] 비용 분석
- [ ] 사용자 피드백 수집
- [ ] 로드맵 업데이트
- [ ] 팀 성과 평가

---

**이 워크플로우 가이드는 MKM Lab의 모든 작업의 기준이 되며, 정기적으로 검토하고 업데이트됩니다.**

**마지막 업데이트: 2024년 12월**
**다음 검토 예정: 2025년 3월** 