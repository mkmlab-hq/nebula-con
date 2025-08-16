# Google Cloud Storage 설정 및 SciSpace 데이터 업로드 가이드

## 🚀 **Google Cloud Storage 설정**

### **1단계: Google Cloud 프로젝트 생성**

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com 접속
   - Google 계정으로 로그인

2. **새 프로젝트 생성**
   ```
   프로젝트 이름: mkm-lab-research
   프로젝트 ID: mkm-lab-research-xxxxx
   ```

3. **Cloud Storage API 활성화**
   - API 및 서비스 → 라이브러리
   - "Cloud Storage" 검색 후 활성화

### **2단계: 서비스 계정 키 생성**

1. **서비스 계정 생성**
   ```
   IAM 및 관리 → 서비스 계정
   → "서비스 계정 만들기"
   → 이름: mkm-lab-storage-account
   → 설명: MKM Lab 연구 데이터 저장용
   ```

2. **권한 부여**
   ```
   역할: Storage 관리자 (Storage Admin)
   또는 Storage 객체 관리자 (Storage Object Admin)
   ```

3. **키 파일 다운로드**
   ```
   서비스 계정 → 키 → 키 추가 → JSON
   → 다운로드된 파일을 안전한 위치에 저장
   예: F:\workspace\mkm-analysis-engine\config\gcp-service-account.json
   ```

### **3단계: Storage 버킷 생성**

1. **Cloud Storage 버킷 생성**
   ```
   Cloud Storage → 버킷
   → "버킷 만들기"
   → 이름: mkm-lab-research-data
   → 위치: asia-northeast3 (서울)
   → 클래스: Standard
   → 액세스 제어: 균등하게 적용
   ```

2. **버킷 권한 설정**
   ```
   권한 → 주 구성원 추가
   → 서비스 계정: mkm-lab-storage-account@mkm-lab-research-xxxxx.iam.gserviceaccount.com
   → 역할: Storage 객체 관리자
   ```

## 📦 **필요한 Python 패키지 설치**

```bash
pip install google-cloud-storage google-auth pandas
```

## 🔧 **환경 변수 설정**

### **Windows PowerShell**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="F:\workspace\mkm-analysis-engine\config\gcp-service-account.json"
```

### **Windows CMD**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=F:\workspace\mkm-analysis-engine\config\gcp-service-account.json
```

## 📊 **SciSpace 데이터 처리 및 업로드**

### **1단계: SciSpace에서 데이터 추출**

1. **SciSpace AI 에이전트 실행**
   - 체계적 문헌 검토 (Systematic Literature Review)
   - 연구 주제: "U-LMA Algorithm rPPG"
   - 결과물: 50개 논문 선택

2. **데이터 내보내기**
   - "Export" 또는 "Download" 기능 사용
   - JSON 또는 CSV 형식으로 다운로드

### **2단계: 데이터 처리 스크립트 실행**

```python
# scispace_upload_example.py
from collectors.scispace_data_processor import SciSpaceDataProcessor

# Google Cloud 설정
credentials_path = "config/gcp-service-account.json"
bucket_name = "mkm-lab-research-data"

# 프로세서 초기화
processor = SciSpaceDataProcessor(
    gcp_credentials_path=credentials_path,
    bucket_name=bucket_name
)

# SciSpace에서 추출한 데이터 (예시)
scispace_data = [
    {
        "title": "Wavelet based motion artifact removal for ECG signals",
        "summary": "This paper presents a novel approach...",
        "authors": ["Author1", "Author2"],
        "published_date": "2017-08-19",
        "doi": "10.1234/example.doi",
        "conclusions": "The wavelet-based approach shows...",
        "methods_used": "Wavelet transform, Signal processing",
        "results": "95% accuracy in artifact removal",
        "confidence_score": 0.85
    }
    # ... 더 많은 논문 데이터
]

# 처리 및 업로드
result = processor.process_and_upload(
    scispace_data, 
    "U-LMA Algorithm rPPG"
)

print(f"처리 결과: {result}")
```

### **3단계: 실행 명령**

```bash
cd F:\workspace\mkm-analysis-engine
python collectors/scispace_data_processor.py
```

## 📁 **저장 구조**

### **로컬 저장**
```
mkm-analysis-engine/
├── data/
│   └── scispace_processed/
│       ├── scispace_U-LMA_Algorithm_rPPG_20241207_143022.json
│       ├── scispace_U-LMA_Algorithm_rPPG_20241207_143022.csv
│       └── duplicate_check.db
```

### **Google Cloud Storage**
```
gs://mkm-lab-research-data/
└── scispace_research/
    ├── scispace_U-LMA_Algorithm_rPPG_20241207_143022.json
    ├── scispace_Voice_Analysis_20241207_150000.json
    └── scispace_Facial_Analysis_20241207_160000.json
```

## 🔍 **데이터 확인**

### **Google Cloud Console에서 확인**
1. Cloud Storage → 버킷 → mkm-lab-research-data
2. scispace_research 폴더 클릭
3. 업로드된 파일들 확인

### **로컬에서 확인**
```python
import json
import pandas as pd

# JSON 파일 읽기
with open('data/scispace_processed/scispace_U-LMA_Algorithm_rPPG_20241207_143022.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"총 논문 수: {len(data)}")
print(f"첫 번째 논문: {data[0]['title']}")

# CSV 파일 읽기
df = pd.read_csv('data/scispace_processed/scispace_U-LMA_Algorithm_rPPG_20241207_143022.csv')
print(f"CSV 데이터 형태: {df.shape}")
```

## ⚠️ **주의사항**

1. **보안**: 서비스 계정 키 파일을 절대 GitHub에 업로드하지 마세요
2. **비용**: Google Cloud Storage 사용량에 따라 비용이 발생할 수 있습니다
3. **백업**: 중요한 데이터는 여러 위치에 백업하세요
4. **권한**: 서비스 계정에 필요한 최소 권한만 부여하세요

## 🚀 **다음 단계**

1. **SciSpace에서 실제 데이터 추출**
2. **데이터 처리 스크립트 실행**
3. **Google Cloud에 업로드 확인**
4. **RAG 시스템에 통합**
5. **프로메테우스 두뇌에 주입** 