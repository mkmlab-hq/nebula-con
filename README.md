# NebulaCon Data Quality Metrics & Axes Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/mkmlab-v2/nebula-con)

**NebulaCon**은 데이터 품질과 분포 특성을 다축(axes) 분석으로 평가하는 Python 패키지입니다.

## 🚀 Quick Start

### 설치
```bash
# 개발 모드로 설치
pip install -e .

# 또는 PyPI에서 설치 (향후)
pip install nebula-axes
```

### 기본 사용법

#### 1. Axes 메트릭 계산
```bash
nebula-axes-run --input data/raw/sample.csv --out metrics/axes_run.json
```

#### 2. Retention 메트릭 계산
```bash
nebula-retention-run --base data/raw/base.csv --shifted data/raw/shifted.csv --out metrics/retention_run.json
```

#### 3. 전체 메트릭 분석
```bash
nebula-metrics-full --input data/raw/base.csv --shifted data/raw/shifted.csv --out metrics/full_report.json
```

## 📊 메트릭 축 (Axes)

### A축: Temporal Stability
- **st_var_ratio**: Rolling variance ratio to global variance
- **seasonal_corr**: Autocorrelation at seasonal lag
- **psi_trigger_rate**: Population Stability Index

### B축: Distributional Shape
- **sk_k_score**: |skew| + |kurtosis - 3| (deviation from normal)
- **outlier_impact**: Proportion of outliers (IQR-based)
- **dip_stat**: Hartigan Dip Test statistic (unimodality)

### C축: Semantic Density
- **intra_cluster_density**: Mean intra-cluster distance / global reference
- **silhouette_approx**: Approximate silhouette score
- **density_k**: Optimal number of clusters

### D축: Cross-Domain Transferability
- **macro_f1_base**: Baseline macro F1-score
- **retention_zero_shot**: Zero-shot performance retention
- **retention_retrained**: Retrained performance retention

## 🛠️ CLI 옵션

### 공통 옵션
- `--input`, `-i`: 입력 CSV 파일 경로
- `--out`, `-o`: 출력 JSON 파일 경로
- `--feature-col`, `-f`: 분석할 특성 컬럼명 (기본값: feat_a)
- `--min-samples`: 최소 샘플 수 요구사항
- `--json-out-dir`: 출력 디렉토리 지정

### 예시
```bash
# 특성 컬럼 변경
nebula-axes-run --input data.csv --feature-col feature_1 --out results.json

# 출력 디렉토리 지정
nebula-axes-run --input data.csv --json-out-dir results/ --out axes.json
```

## 📁 프로젝트 구조

```
nebula-con/
├── src/nebula_axes/           # 메인 패키지
│   ├── cli/                   # CLI 엔트리포인트
│   │   ├── run_axes.py       # Axes 메트릭 CLI
│   │   ├── run_retention.py  # Retention 메트릭 CLI
│   │   └── run_full.py       # 전체 메트릭 CLI
│   ├── metrics/               # 메트릭 계산 모듈
│   │   └── core/             # 핵심 메트릭
│   │       ├── temporal.py   # A축 (temporal)
│   │       ├── drift.py      # A축 (drift)
│   │       ├── shape.py      # B축 (shape)
│   │       ├── density.py    # C축 (density)
│   │       └── retention.py  # D축 (retention)
│   └── utils/                 # 유틸리티 함수
├── config/                     # 설정 파일
├── docs/                       # 문서
├── tests/                      # 테스트
└── data/                       # 샘플 데이터
```

## 🔧 개발 환경

### 의존성
- Python 3.8+
- numpy, pandas, scikit-learn, scipy

### 개발 의존성 설치
```bash
pip install -e ".[dev]"
```

### 테스트 실행
```bash
pytest
```

## 📈 사용 예시

### Python 코드에서 직접 사용
```python
from nebula_axes import compute_temporal_metrics, compute_shape_metrics
import pandas as pd

# 데이터 로드
df = pd.read_csv('data.csv')
s = df['feature'].astype(float)

# 메트릭 계산
temporal = compute_temporal_metrics(s)
shape = compute_shape_metrics(s)

print(f"Temporal stability: {temporal}")
print(f"Distribution shape: {shape}")
```

### CLI로 배치 처리
```bash
# 여러 파일 처리
for file in data/*.csv; do
    nebula-axes-run --input "$file" --out "results/$(basename "$file" .csv)_metrics.json"
done
```

## 📚 문서

- [메트릭 스키마](docs/metrics_schema.md) - 모든 메트릭 필드 정의
- [재현 가이드](docs/REPRO_TIER0.md) - Tier0 환경 설정 및 실행
- [기여 가이드](CONTRIBUTING.md) - 개발 참여 방법

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🏷️ 버전

- **v0.2.0** (현재): CLI + 패키징 + 모듈화 완성
- **v0.1.0**: 기본 메트릭 구현

## 📞 연락처

- **MKM Lab** - mkmlab@example.com
- **GitHub Issues**: [https://github.com/mkmlab-v2/nebula-con/issues](https://github.com/mkmlab-v2/nebula-con/issues)

---

**NebulaCon** - 데이터 품질을 다축으로 분석하는 강력한 도구 🚀
