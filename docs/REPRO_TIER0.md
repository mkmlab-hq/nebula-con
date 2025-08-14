# Tier0 Reproduction Guide

이 문서는 NebulaCon Tier0 환경에서 메트릭 계산과 분석을 재현하는 방법을 설명합니다.

## 🎯 Tier0 목표

**Tier0 Exit Criteria (필수 달성):**
- ✅ **axes_registry.json v0.2.0** with 9 micro axes
- ✅ **Working ingest profile JSON** 
- ✅ **Baseline macro_f1 logged** (metrics/baseline_run.json)
- ✅ **Axes feature dump** (stdout or metrics/axes_sample.json)
- ✅ **CI green** (lint+baseline smoke)

## 🚀 Quick Start

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/mkmlab-v2/nebula-con.git
cd nebula-con

# Python 3.8+ 확인
python --version

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 개발 모드로 설치
pip install -e .
```

### 2. 기본 메트릭 계산

```bash
# Axes 메트릭 계산
nebula-axes-run --input data/raw/sample.csv --out metrics/axes_run.json

# 결과 확인
cat metrics/axes_run.json
```

### 3. 전체 메트릭 분석

```bash
# Retention 메트릭 계산 (샘플 데이터 복사)
cp data/raw/sample.csv data/raw/sample_shifted.csv

# 전체 분석 실행
nebula-metrics-full --input data/raw/sample.csv --shifted data/raw/sample_shifted.csv --out metrics/full_report.json

# 결과 확인
cat metrics/full_report.json
```

## 📊 메트릭 축별 상세 분석

### A축: Temporal Stability

**st_var_ratio** (Rolling Variance Ratio)
- **의미**: Rolling variance / Global variance
- **범위**: 0.0 ~ ∞
- **해석**: 
  - < 0.5: 매우 안정적
  - 0.5 ~ 1.0: 안정적
  - > 1.0: 불안정 (drift 의심)

**seasonal_corr** (Seasonal Correlation)
- **의미**: Seasonal lag에서의 autocorrelation
- **범위**: -1.0 ~ 1.0
- **해석**:
  - < 0.1: 계절성 없음
  - 0.1 ~ 0.3: 약한 계절성
  - > 0.3: 강한 계절성

**psi_trigger_rate** (Population Stability Index)
- **의미**: Baseline vs Current distribution drift
- **범위**: 0.0 ~ ∞
- **해석**:
  - < 0.1: 안정적
  - 0.1 ~ 0.25: 주의 필요
  - > 0.25: drift 감지

### B축: Distributional Shape

**sk_k_score** (Skew + Kurtosis Score)
- **의미**: |skew| + |kurtosis - 3|
- **범위**: 0.0 ~ ∞
- **해석**:
  - < 1.0: 정규분포에 가까움
  - 1.0 ~ 3.0: 약간의 편차
  - > 3.0: 정규분포와 큰 차이

**outlier_impact** (Outlier Ratio)
- **의미**: IQR 기반 이상치 비율
- **범위**: 0.0 ~ 1.0
- **해석**:
  - < 0.05: 이상치 거의 없음
  - 0.05 ~ 0.1: 적당한 이상치
  - > 0.1: 많은 이상치

**dip_stat** (Hartigan Dip Test)
- **의미**: Unimodality 검정 통계량
- **범위**: 0.0 ~ 1.0
- **해석**:
  - < 0.02: Unimodal
  - 0.02 ~ 0.05: 잠재적 multimodal
  - > 0.05: Multimodal

### C축: Semantic Density

**intra_cluster_density** (Intra-cluster Density)
- **의미**: Intra-cluster distance / Global reference
- **범위**: 0.0 ~ 1.0
- **해석**:
  - < 0.5: 강한 클러스터링
  - 0.5 ~ 0.8: 중간 클러스터링
  - > 0.8: 약한 클러스터링

**silhouette_approx** (Silhouette Score)
- **의미**: 클러스터 분리 품질
- **범위**: -1.0 ~ 1.0
- **해석**:
  - < 0.1: 클러스터 분리 부족
  - 0.1 ~ 0.3: 적당한 분리
  - > 0.3: 좋은 분리

**density_k** (Optimal Clusters)
- **의미**: 최적 클러스터 수
- **범위**: 2 ~ 6
- **해석**: 데이터의 자연스러운 그룹핑 수

### D축: Cross-Domain Transferability

**macro_f1_base** (Baseline F1-Score)
- **의미**: 원본 데이터에서의 성능
- **범위**: 0.0 ~ 1.0
- **해석**: 높을수록 좋은 성능

**retention_zero_shot** (Zero-shot Retention)
- **의미**: Zero-shot 성능 유지율
- **범위**: 0.0 ~ ∞
- **해석**:
  - < 0.8: 성능 저하 심각
  - 0.8 ~ 0.9: 적당한 저하
  - > 0.9: 성능 유지

**retention_retrained** (Retrained Retention)
- **의미**: 재학습 후 성능 유지율
- **범위**: 0.0 ~ ∞
- **해석**: 높을수록 domain adaptation 성공

## 🔧 고급 사용법

### 1. 커스텀 특성 컬럼 분석

```bash
# 다른 특성 컬럼 분석
nebula-axes-run --input data/raw/sample.csv --feature-col feat_b --out metrics/axes_feat_b.json
```

### 2. 배치 처리

```bash
# 여러 파일 처리
for file in data/raw/*.csv; do
    basename=$(basename "$file" .csv)
    nebula-axes-run --input "$file" --out "metrics/${basename}_axes.json"
done
```

### 3. Python 코드에서 직접 사용

```python
from nebula_axes import compute_temporal_metrics, compute_shape_metrics
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/raw/sample.csv')
s = df['feat_a'].astype(float)

# 메트릭 계산
temporal = compute_temporal_metrics(s)
shape = compute_shape_metrics(s)

print(f"Temporal: {temporal}")
print(f"Shape: {shape}")
```

## 📈 결과 해석 가이드

### 1. 데이터 품질 평가

**우수한 데이터 품질:**
- `st_var_ratio` < 0.8
- `psi_trigger_rate` < 0.1
- `dip_stat` < 0.02
- `silhouette_approx` > 0.2

**주의가 필요한 데이터:**
- `st_var_ratio` > 1.2
- `psi_trigger_rate` > 0.25
- `dip_stat` > 0.05
- `outlier_impact` > 0.1

### 2. Drift 감지

**Drift 의심 지표:**
- `psi_trigger_rate` > 0.25
- `st_var_ratio` > 1.0
- `seasonal_corr` 변화 > 0.2

### 3. 클러스터링 품질

**좋은 클러스터링:**
- `silhouette_approx` > 0.3
- `intra_cluster_density` < 0.6
- `density_k` = 2~4

## 🧪 검증 및 테스트

### 1. 기본 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 테스트
pytest tests/test_metrics/test_shape.py

# 커버리지 포함
pytest --cov=src/nebula_axes
```

### 2. 메트릭 범위 검증

```bash
# PowerShell 스크립트 사용
.\dev.ps1 verify

# 또는 개별 실행
.\dev.ps1 test
.\dev.ps1 lint
.\dev.ps1 axes
```

### 3. 성능 벤치마크

```bash
# 대용량 데이터 테스트 (선택사항)
python -c "
import time
import pandas as pd
import numpy as np
from nebula_axes import compute_axes

# 대용량 데이터 생성
n_samples = 10000
df = pd.DataFrame({
    'feat_a': np.random.normal(0, 1, n_samples),
    'feat_b': np.random.normal(0, 1, n_samples)
})

# 성능 측정
start_time = time.time()
metrics = compute_axes(df)
end_time = time.time()

print(f'10K samples 처리 시간: {end_time - start_time:.2f}초')
print(f'계산된 메트릭: {len(metrics)}개')
"
```

## 🚨 문제 해결

### 1. 일반적인 오류

**ImportError: No module named 'nebula_axes'**
```bash
# 패키지 재설치
pip install -e .
```

**FileNotFoundError: data/raw/sample.csv**
```bash
# 샘플 데이터 확인
ls data/raw/
# 또는 샘플 데이터 생성
python -c "
import pandas as pd
import numpy as np
df = pd.DataFrame({
    'feat_a': np.random.normal(0, 1, 500),
    'feat_b': np.random.normal(0, 1, 500)
})
df.to_csv('data/raw/sample.csv', index=False)
print('샘플 데이터 생성 완료')
"
```

**MemoryError (대용량 데이터)**
```bash
# 데이터 샘플링
python -c "
import pandas as pd
df = pd.read_csv('data/raw/large_data.csv')
df_sample = df.sample(n=1000, random_state=42)
df_sample.to_csv('data/raw/sample.csv', index=False)
print('샘플링 완료')
"
```

### 2. 성능 최적화

**느린 계산 속도:**
- 데이터 크기 확인: `wc -l data/raw/sample.csv`
- 메모리 사용량 모니터링
- 필요시 데이터 샘플링

**메모리 부족:**
- 가상 메모리 증가
- 데이터 청크 단위 처리
- 불필요한 컬럼 제거

## 📊 결과 저장 및 공유

### 1. 메트릭 결과 저장

```bash
# 결과 디렉토리 생성
mkdir -p results/$(date +%Y%m%d)

# 메트릭 계산 및 저장
nebula-axes-run --input data/raw/sample.csv --json-out-dir results/$(date +%Y%m%d) --out axes_metrics.json
nebula-metrics-full --input data/raw/sample.csv --shifted data/raw/sample_shifted.csv --json-out-dir results/$(date +%Y%m%d) --out full_report.json
```

### 2. 결과 요약 생성

```bash
# Python으로 결과 요약
python -c "
import json
import glob

# 최신 결과 파일 찾기
result_files = glob.glob('results/*/full_report.json')
latest_file = max(result_files, key=lambda x: x.split('/')[1])

with open(latest_file, 'r') as f:
    data = json.load(f)

print('=== NebulaCon 메트릭 요약 ===')
print(f'분석 일시: {data[\"metadata\"][\"version\"]}')
print(f'기본 샘플: {data[\"metadata\"][\"base_samples\"]}')
print(f'이동 샘플: {data[\"metadata\"][\"shifted_samples\"]}')

axes = data['axes_metrics']
print(f'\\n=== 핵심 메트릭 ===')
print(f'PSI: {axes[\"psi_trigger_rate\"]:.4f}')
print(f'Dip Stat: {axes[\"dip_stat\"]:.4f}')
print(f'Silhouette: {axes[\"silhouette_approx\"]:.4f}')

print('\\n✅ 분석 완료!')
"
```

## 🔮 다음 단계

### Phase 4: Threshold Enforcement + CI
- 메트릭 범위 자동 검증
- GitHub Actions CI/CD
- 품질 게이트 자동화

### Phase 5: Performance & Meta
- 메트릭 계산 캐싱
- 실행 메타데이터 수집
- 성능 최적화

### Phase 6: Advanced Metrics
- Jensen-Shannon divergence
- Sliding window PSI
- Scenario shift detection

---

**Tier0 완성 축하!** 🎉

이제 안정적인 기반 위에서 고급 기능을 확장할 수 있습니다. 