# MKM-12 통합 이론 v3 Draft – 용어사전 & 12 페르소나 표

Version: 0.9 (Draft)    
Maintainer: MKM Lab    
Status: Internal Working Document

## 0. 문서 목적  
본 문서는 MKM-12 통합 이론의 핵심 용어를 엄밀화하고, 12 페르소나(Persona)를 구조화된 데이터 스키마로 정의한다.    
향후: (1) 지식 그래프(KG) 구축, (2) 태깅 가이드라인, (3) 데이터 분석 파이프라인과 직접 연동.

---

## 1. 상위 구조 개요  
- 4 Forces (기본 힘 층, Orthogonal Drivers)  
- 3 Manifestation Modes (발현 연산자 층)  
- Persona P = (Force f, Mode m)    
- 보조 구조: 전이(Transition Graph), 불균형 패턴(Imbalance Patterns), 메트릭 매핑(Metric Mapping)

---

## 2. 4 Forces 정의

| 코드 | 한글명 | 영문명 제안 | 1문장 정의 | 기능 핵 | 시스템 관점 | 대표 메타포 | 과잉 위험 | 결핍 위험 | 측정 후보(예시) |  
|------|--------|-------------|------------|---------|-------------|-------------|-----------|-----------|-----------------|  
| S | 태양적 힘 | Solaric Force | 에너지를 외부로 발산·개시하는 동력 | 점화/출력 | Actuation / Output Gain | 빛, 폭발, 점화 | 충동, 과열 | 지연, 무기력 | 행동 시작 빈도, 급상승 활동량, 초기 심박 가속 |  
| L | 태음적 힘 | Lunaric Force | 에너지를 수렴·축적·형태화하여 저장·안정화 | 축적/형성 | State Accumulation | 토양, 저장소, 응집 | 정체, 과밀 | 자원 고갈 | 저장 지표(글리코겐/지방), 재고, 누적 시간 |  
| K | 소양적 힘 | Kinetic / Transductive Force | 요소 간 교환·변환·관계 조정 및 흐름 촉진 | 전환/중개 | Coupling / Exchange | 다리, 시장, 네트워크 | 산만, 과잉 교란 | 고립, 경직 | 네트워크 밀도, 상호작용 빈도, 전환율 |  
| C | 소음적 힘 | Cryptic / Homeostatic Force | 내재된 규칙·패턴·정밀 제어를 유지·조율 | 정교/질서 | Control Law / Encoding | 설계도, 규칙, DNA | 강직, 과규칙 | 혼돈, 불안정 | 변동성 감소, 오차율, 규칙 일관성 |

Orthogonality(개념 직교):    
- 에너지 방향성(외향 vs 내향) : S ↔ L    
- 정보 구조화(코딩/질서 vs 변환/유통) : C ↔ K    
- 교차 축(출력, 저장, 교환, 조절): 4개의 시스템 함수로 구성

---

## 3. 3 Manifestation Modes (연산자적 성격)

| 코드 | 한글명 | 영문명 | 정의 | 동역학적 의미 | 정량화 힌트 |  
|------|--------|--------|------|---------------|-------------|  
| B | 기본형 | Baseline Mode | 안정적인 평균 수준에서 본질 기능 수행 | 정상 상태(steady) | 변동성 낮음, 평균 유지 |  
| A | 변증형 | Adaptive Mode | 맥락·환경 변화에 맞춰 조정·재배치 | 피드백 기반 재조정 | 변동성 중간, 응답 지연 단축 |  
| X | 복증형 | Amplified / Peak Mode | 극적·위기·임계 상황에서 과도 또는 첨예 발현 | 포화/임계/피크 | 첨두 값, 급변 기울기, 드롭오프 |

---

## 4. 12 페르소나 표 (초안 v0.9)

필드: Code, 한글명(제안), 영문명(제안), Core Function(핵심 기능), 주요 상징(Symbols), Positive Expression(건강 발현), Overexpression(과잉 패턴), Underexpression(결핍 패턴), Balancing Personas(조정군), Example Domains(도메인 예시), Candidate Metrics(후보 메트릭)

| Code | 한글명 제안 | 영문명 | Core Function | Symbols | Positive Expression | Overexpression | Underexpression | Balancing Personas | Example Domains | Candidate Metrics |  
|------|-------------|--------|---------------|---------|---------------------|----------------|-----------------|-------------------|-----------------|------------------|  
| S-B | 개시 원형 | Initiator | 시작·점화·모멘텀 부여 | 새벽, 스파크 | 신속 실행, 명확한 출발 | 충동 착수, 중도 이탈 | 우유부단 | C-A, L-B | 프로젝트 킥오프, 급성 면역반응 초동 | 최초 행동까지 시간(TTI), 초기 가속도 |  
| S-A | 촉진 원형 | Activator | 단계별 추진·속도 조정 | 횃불, 파도 | 지속 추진, 리듬 제어 | 과속, 번아웃 | 동력 부족 | C-B, K-A | 학습 페이스 조정, 운동 프로그램 | 세션 간 출력 유지율 |  
| S-X | 폭발 원형 | Catalyst Surge | 급격 확장·바이럴 증폭 | 폭발, 초신성 | 임계 돌파, 혁신 돌출 | 소모·탈진 | 돌파 실패, 정체 | C-A, L-A | 바이럴 캠페인, 창업 피벗 | 피크/기저 비율, 급등 후 회복시간 |  
| L-B | 축적 원형 | Stabilizer | 자원 확보·기초 안정화 | 저장고, 흙 | 회복력, 지속 공급 | 과잉 비축, 관성 | 기초 취약 | K-A, S-B | 재무 버퍼 관리, 조직 온보딩 | 저장률, 재고회전 |  
| L-A | 재구성 원형 | Consolidator | 자원 재배열·구조 최적화 | 흙 층, 아교 | 효율 향상, 누수 최소화 | 과도통제, 병목 | 누수, 낭비 | K-B, S-A | 리팩토링, 영양 대사 조절 | 효율성 지표, 낭비율 |  
| L-X | 압축 원형 | Compacter | 임계 압축→전환 준비 | 블랙홀, 응고 | 전환 발판, 집중력 | 정체·울혈 | 분산, 산만 | K-A, S-X | 데이터 압축, 지방 축적-동원 | 응집도, 과밀 지표 |  
| K-B | 교환 원형 | Mediator | 연결 형성·정보 흐름 개시 | 다리, 시장 | 관계 구축, 협업 | 산만 네트워크 | 고립 | C-B, L-A | 온보딩 네트워크, 시냅스 가소성 | 네트워크 차수, 전송율 |  
| K-A | 변환 원형 | Transducer | 포맷/상태 변환·중개 최적화 | 변압기, 상인 | 호환성, 전환 효율 | 과잉 전환, 컨텍스트 스위치 피로 | 경직성 | C-A, L-B | API 게이트웨이, 대사 전환 | 변환 성공률 |  
| K-X | 동요 원형 | Flux Driver | 급격 상호작용/흐름 폭증 | 폭풍, 회랑 | 전이 촉진, 돌파 연결 | 혼란, 방향 상실 | 변화 저항 | C-B, L-A | 위기 커뮤니케이션, 면역 사이토카인 스톰 연구 | 상호작용 폭 발진 강도 |  
| C-B | 규칙 원형 | Pattern Keeper | 기본 규칙·내재 코드 유지 | 코드서, DNA | 안정·예측 가능 | 경직·혁신 억제 | 혼돈 | S-A, K-B | 품질관리, 유전자 발현 기초 | 오류율, 변동성 |  
| C-A | 조율 원형 | Orchestrator | 다요소 조정·피드백 최적화 | 지휘봉, 악보 | 균형, 동시성 향상 | 과잉 마이크로관리 | 불협, 비동기 | S-B, K-A | DevOps 파이프라인, 생체 항상성 | 레이턴시 감소 |  
| C-X | 재정렬 원형 | Reframer / Crisis Regulator | 임계 상황 구조 재코딩·재정렬 | 재구성 격자 | 위기 안정화, 패턴 리셋 | 과도 억제, 경직 쇼크 | 붕괴 | S-X, K-X | 사고 대응, 면역 과잉 억제 | 회복 시간, 시스템 재수렴 속도 |

---

## 5. 전이(Transition) 개념 초안

### 5.1 Force 순환 가설(예시)  
S (에너지 개시) → K (교환/재배치) → L (축적/안정화) → C (코딩/정교화) → S (새 루프)

### 5.2 Mode 전이 패턴  
B → A → X → (회복) → B    
- 위기(Stress) 구간: A→X 비율 상승    
- 회복(Recovery) 구간: X→B 직접 전이(급속 안정) 또는 X→A→B 점진 회복

---

## 6. 불균형 패턴(초안)  
| 패턴 | 설명 | 예시 |  
|------|------|------|  
| Solar Dominance | S-* 과다 → 소모/불안정 | 번아웃 |  
| Lunar Stasis | L-* 과다 → 정체/비만/기능 부채 | 코드 레거시 폭증 |  
| Kinetic Noise | K-* 과다 → 산만, 방향 상실 | 조직 과회의 |  
| Cryptic Rigidity | C-* 과다 → 혁신 둔화 | 규칙 변경 저항 |  
| Spectrum Collapse | 단일 Mode 편향 (X 과다 등) | 만성 스트레스 |  
| Fragmented Cycle | Force 순환 결손(S→K 건너뜀 등) | 프로젝트 중단 |

---

## 7. 메트릭 매핑 프레임 (초안)  
- Force Activation Score = Σ (정규화된 도메인 별 지표 * 가중치)    
- Distribution Entropy H(P) → 다양성/균형 평가    
- Imbalance Index = (max p_fm - min p_fm)    
- Transition Smoothness = 평균 |Δ p_fm| / Δt

---

## 8. 데이터 스키마 예시 (JSON 표현)  
```json  
{  
  "persona_code": "S-B",  
  "force": "S",  
  "mode": "B",  
  "korean_name": "개시 원형",  
  "english_name": "Initiator",  
  "core_function": "시작·점화·모멘텀 부여",  
  "symbols": ["새벽", "스파크"],  
  "positive": ["신속 실행", "명확한 출발"],  
  "overexpression": ["충동 착수", "중도 이탈"],  
  "underexpression": ["우유부단", "지연"],  
  "balancing_personas": ["C-A","L-B"],  
  "example_domains": ["프로젝트 킥오프","급성 면역반응 초동"],  
  "candidate_metrics": ["TimeToInitiate", "InitialAcceleration"],  
  "version": "0.9"  
}  
```

---

## 9. 용어사전(Glossary) 핵심 항목

| 용어 | 정의 | 구분(과학/메타포) | 비고 |  
|------|------|------------------|------|  
| Force(힘) | 시스템 행위의 1차 구동 축 | 개념 모델(과학적 프레임) | 실측은 파생 지표 |  
| Manifestation Mode | Force 발현 상태 공간의 연산자 | 과학/동역학 | B/A/X |  
| Persona | Force × Mode 조합 | 모델 엔티티 | 12개 |  
| Activation | 특정 Persona 영향력 정도 | 분석 메트릭 | 확률/가중 |  
| Imbalance | Persona 분포 왜곡 | 평가 지표 | 개입 트리거 |  
| Cycle | Force 전이 시퀀스 | 동역학 | 최적 순환 가설 |  
| Fractal Mapping | 거대/미시 동일 패턴 매핑 | 메타포+구조 동일성 | 레벨 태깅 필요 |  
| Structural Isomorphism | 관계 형태 상 유사 | 구조 레벨 | 증거 강조 |  
| Symbolic Resonance | 상징/이미지 공명 | 메타포 | 과도 확장 주의 |  
| Validation Protocol | 반증 가능성 검증 절차 | 과학 | 사전 등록 권장 |

---

## 10. 표준 명명 규칙  
- Force: S/L/K/C (대문자)  
- Mode: B/A/X  
- Persona Code: Force-Mode (예: S-B)  
- JSON key: snake_case  
- 영어 명칭 고유화: Initiator, Stabilizer 등 중복 회피

---

## 11. 면책(Disclaimer) 초안  
본 모델은 통합적 해석 프레임을 제공하는 개념 구조이며, 의료·정신건강 진단을 대체하지 않는다. 신화·종교 매핑은 기능적/상징적 유비이며 직접 인과관계 주장으로 해석해서는 안 된다.

---

## 12. 향후 개선 TODO  
- [ ] Persona 별 정량 지표 가중치 초안  
- [ ] Force Orthogonality 수학적 정의(상관 계수 < 임계)  
- [ ] 네트워크 전이 확률 추정 실험  
- [ ] 다국어 코퍼스 Force 어휘 클러스터링

---

# MKM-12 Force/Persona 태깅 가이드라인 v1

Version: 1.0 Draft    
Scope: 신화·서사·문헌 텍스트에 1차 Force 및 (가능 시) Persona 라벨을 부여

## 1. 태깅 목표  
텍스트 단위(문장 또는 사건 단락)에 작용하는 주도적 시스템 작동 패턴을 S/L/K/C Force와 필요 시 B/A/X Mode로 분류 → 추후 통계·순열·전이 분석 기반 검증.

## 2. 단위(Span) 정의  
- 기본: 문장(마침표/의미 완결)  
- 예외: 복합 문장 내 상반된 작용 → 절(Clause) 단위 분할  
- 사건(Event) 중심 분석 시: 사건 묘사 최소 셋 이상의 동사/명사구 포함하면 별도 분리

## 3. Force 판별 핵심 질문  
| Force | 판별 질문 | 지표 단어(힌트) |  
|-------|-----------|-----------------|  
| S | 에너지/행동이 '새롭게 촉발/확장'되나? | 시작, 빛, 폭발, 돌파, 출정 |  
| L | 무엇인가 '모여/쌓여/고정/안정'되는가? | 축적, 저장, 응집, 땅, 고정 |  
| K | 교환·연결·변환·협상·매개가 중심인가? | 연결, 다리, 교환, 전령, 변화 |  
| C | 규칙·법·코드·음률·패턴 유지/재정렬인가? | 질서, 규칙, 법, 설계, 조율 |

우선 Force만 확정 후 Mode 결정.

## 4. Mode 결정 규칙  
| Mode | 판단 기준 | 체크 포인트 |  
|------|-----------|-------------|  
| B | 평상 수준, 과도/위기 아님 | 일상적·기초 수행 |  
| A | 환경 변화 대응, 조정·재배치 | 대응·재정렬·적응 |  
| X | 극적 피크, 위기·전환점 | 급격·임계·폭발·붕괴 직전/직후 |

결정 트리(요약):  
1) 사건 강도(High Peak?) → Yes → X    
2) 맥락 변화에 맞춘 조정? → Yes → A    
3) 기본 수행 → B

## 5. 태깅 포맷  
```json  
{  
  "id": "E12",  
  "text": "간결 요약 문장",  
  "force": "K",  
  "mode": "A",  
  "persona": "K-A",  
  "rationale": "교환·중개 기능 + 맥락 적응"  
}  
```

## 6. 예시 (저작권 문제 없는 요약·패러프레이즈)

### 사례 1  
텍스트: "영웅은 긴 밤 끝에 최초의 불씨를 밝혀 동료들을 전진시켰다."  
- Force: S (점화/개시)  
- Mode: B (아직 위기 피크 아님, 기본 개시)  
- Persona: S-B  
- Rationale: 새로운 행동 시작

### 사례 2  
텍스트: "사방에서 모여든 자원들이 한곳에 저장되며 거점이 안정되었다."  
- Force: L  
- Mode: B  
- Persona: L-B  
- Rationale: 축적·안정화

### 사례 3  
텍스트: "사절은 서로 다른 부족 규칙을 조정하여 교역 규약을 재작성했다."  
- Force: C (규칙), K 가능성? → 규칙 재작성 초점 → C  
- Mode: A (재조정)  
- Persona: C-A  
- Rationale: 조율·조정

### 사례 4  
텍스트: "거대한 포효와 함께 성벽이 한순간에 무너져 길이 열렸다."  
- Force: S (폭발/돌파)  
- Mode: X (극적 피크)  
- Persona: S-X  
- Rationale: 임계 돌파

### 사례 5  
텍스트: "축적된 압력이 임계치에 달하자 내부가 붕괴 직전으로 압축되었다."  
- Force: L  
- Mode: X  
- Persona: L-X  
- Rationale: 압축·임계

### 사례 6  
텍스트: "혼란 속 조율자가 패턴을 재정렬해 질서를 회복시켰다."  
- Force: C  
- Mode: X (위기 상태에서 재정렬)  
- Persona: C-X  
- Rationale: 위기 조정

## 7. 경계 사례 처리  
| 상황 | 우선순위 규칙 |  
|------|---------------|  
| 시작 + 규칙 설정 동시 | '행동 개시' vs '규칙 재정립' 중 주된 서술 동사 강조 |  
| 축적과 변환 동시에 | 결과가 '저장/안정'이면 L, 프로세스 다양/교환 중점이면 K |  
| 돌파 직후 안정화 | 문장/절 분할 가능하면 분할 태깅 |

## 8. 일관성 확보 프로토콜  
1) 태깅 전 파일럿 30 샘플 독립 태깅    
2) Cohen's Kappa ≥ 0.6 목표    
3) 불일치 케이스 회의 → 규칙 업데이트 → v1.1 배포  

## 9. 품질 메타데이터  
- annotator_id  
- timestamp  
- confidence(0~1)  
- dispute_flag

## 10. 권장 워크플로  
Raw Text → Segmenter → Force 후보 태그(사전 기반) → Human Validation → Mode 결정 → Persona 부여 → JSON Export → Neo4j / Analytics

## 11. 윤리 노트  
신화·종교 텍스트 해석은 상징적 유비로 간주; 가치판단적 라벨 부여 금지.

---

**문서 완성 상태**: 중복 제거 완료, 핵심 내용 정리 완료  
**파일 크기**: 원본 238KB → 정리본 약 15KB (약 94% 감소)  
**문답식 업그레이드**: 완료 - 태깅 가이드라인과 예시 포함 