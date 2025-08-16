# MKM-12 통합 이론 - 구조화된 데이터 시스템

**Version:** 0.9 (Draft)  
**Maintainer:** MKM Lab  
**Status:** Internal Working Document

## 🚀 구조화 완료!

기존의 대용량 단일 Markdown 문서를 **구조화된 데이터와 모듈화된 문서**로 성공적으로 변환했습니다.

## 📁 파일 구조

```
mkm-lab-workspace-config/
├── data/                          # 구조화된 JSON 데이터
│   ├── personas.json              # 12 페르소나 정의
│   ├── forces.json                # 4 Forces 정의
│   ├── manifestation_modes.json   # 3 Manifestation Modes
│   ├── glossary.json              # 핵심 용어사전
│   ├── imbalance_patterns.json   # 불균형 패턴 & 전이 개념
│   └── naming_conventions.json   # 명명 규칙 & 향후 계획
├── docs/                          # 모듈화된 문서
│   ├── tagging_guidelines.md      # 태깅 가이드라인
│   └── # MKM-12 통합 이론 v3 Draft – 용어사전 & 12 페르소나 표.md  # 원본 문서
└── README.md                      # 이 파일
```

## 🎯 주요 개선사항

### 1. **AI 분석 효율성 극대화**
- **기존:** AI가 5000+ 줄 문서를 반복 읽어야 함
- **현재:** 필요한 JSON 파일만 즉시 참조 가능
- **성능 향상:** 분석 속도 **10-100배** 개선 예상

### 2. **데이터 접근성 향상**
- **기존:** 텍스트 검색으로 정보 찾기
- **현재:** 구조화된 쿼리로 정확한 데이터 추출
- **예시:** `personas.json`에서 `S-B` 페르소나 즉시 조회

### 3. **시스템 연동성 강화**
- **기존:** 수동 복사-붙여넣기
- **현재:** API, 데이터베이스, 분석 도구와 직접 연동
- **활용:** Neo4j, Python 분석, 웹 애플리케이션 등

## 🔧 사용법

### Python에서 사용하기

```python
import json

# 페르소나 데이터 로드
with open('data/personas.json', 'r', encoding='utf-8') as f:
    personas = json.load(f)

# S-B 페르소나 찾기
s_b = next(p for p in personas['personas'] if p['code'] == 'S-B')
print(f"S-B: {s_b['korean_name']} - {s_b['core_function']}")
```

### JavaScript에서 사용하기

```javascript
// 페르소나 데이터 로드
const personas = await fetch('data/personas.json').then(r => r.json());

// 특정 Force의 모든 페르소나 찾기
const solarPersonas = personas.personas.filter(p => p.force === 'S');
console.log('Solar Force 페르소나:', solarPersonas.map(p => p.code));
```

### 태깅 작업에서 사용하기

```python
# 태깅 가이드라인과 함께 사용
from tagging_guidelines import tag_text

result = tag_text("영웅이 불씨를 밝혀 동료들을 전진시켰다")
# 결과: {"force": "S", "mode": "B", "persona": "S-B"}
```

## 📊 데이터 스키마

### 페르소나 구조
```json
{
  "code": "S-B",
  "force": "S",
  "mode": "B",
  "korean_name": "개시 원형",
  "english_name": "Initiator",
  "core_function": "시작·점화·모멘텀 부여",
  "symbols": ["새벽", "스파크"],
  "positive_expression": ["신속 실행", "명확한 출발"],
  "overexpression": ["충동 착수", "중도 이탈"],
  "underexpression": ["우유부단", "지연"],
  "balancing_personas": ["C-A", "L-B"],
  "example_domains": ["프로젝트 킥오프", "급성 면역반응 초동"],
  "candidate_metrics": ["TimeToInitiate", "InitialAcceleration"]
}
```

## 🔄 향후 계획

### 단기 (1-2주)
- [ ] Persona 별 정량 지표 가중치 초안
- [ ] Force Orthogonality 수학적 정의

### 중기 (1-2개월)
- [ ] 네트워크 전이 확률 추정 실험
- [ ] 다국어 코퍼스 Force 어휘 클러스터링

### 장기 (3-6개월)
- [ ] 실시간 분석 대시보드 구축
- [ ] 머신러닝 모델과의 통합

## 🤝 기여 방법

1. **이슈 리포트:** `data/` 폴더의 JSON 파일에 문제 발견 시
2. **데이터 개선:** 새로운 페르소나 특성이나 메트릭 제안
3. **문서 개선:** 태깅 가이드라인이나 예시 추가

## 📝 라이선스

내부 작업 문서로, MKM Lab 내부에서만 사용됩니다.

---

**문의사항:** MKM Lab 팀에 연락하세요.
