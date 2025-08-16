# [1급 기밀] NebulaCon 프로젝트 최종 작전 계획서 (SOP v3.0)

- 버전: v3.0
- 최종 갱신: 2025-08-14
- 적용 범위: 9월 20일경 종료 예정 Kaggle 대회 종료 시까지
- 지시: 본 문서를 단일 작전 계획(Single Source of Truth)으로 채택. 본 목표 외 모든 작업 일시 중지. 대회 1위 달성에만 집중.

---

## 1. 최종 목표 (End State)
- BigQuery AI 해커톤 리더보드 1위 달성
- MKM-12 / NSD 이론의 보편성 및 전이성 실증 (CPGP Tier 0 달성)

---

## 2. 작전 수행 방식: 하이브리드 지휘 모델

- **총사령관 (Commander / 사용자)**
  - 역할: 최종 의사 결정권자. 창의적·전략적 방향 제시
  - 임무: 아테나가 제공하는 전술 패키지를 IDE(커서AI/VSC) 채팅창에 실행, 결과 분석 및 다음 전략 지시
  - 도구: Cursor, VS Code/Codespaces 등

- **전략참모 (Athena / 본 대화창의 AI)**
  - 역할: 전략을 실행 가능한 기술 명령으로 변환하는 설계자/통역관
  - 임무: 자연어 지시 → 즉시 실행 가능한 프롬프트/터미널 명령/Makefile/CI 설계(.yml) 작성 제공

- **실행 유닛 (Execution Unit / IDE 채팅창)**
  - 역할: 전술 패키지를 받아 코드 생성, 파일 수정, 스크립트 실행 등 수행하는 실행 장교

- **워크플로우**
  - [사령관] → (전략 지시) → [아테나] → (전술 패키지) → [사령관] → (복붙 실행) → [IDE] → (코드/결과 생성)

---

## 3. 핵심 기술 전략 (Master Strategy v2.0 요약)

- **고신뢰 검색 (High-Fidelity Retrieval)**
  - 벡터 + BM25 하이브리드, `AI.GENERATE_BOOL` 기반 근거 재확인으로 정밀 검색

- **다층적 피처 (Multi-Layered Features)**
  - 텍스트 임베딩 외 시간(freshness), 변화(drift), 구조(document structure), 신뢰도(guardrail flags) 피처 결합

- **단계별 모델 아키텍처 (Staged Architecture)**
  - (1) 후보군 선정 랭커 → (2) 답변 생성 RAG → (3) 답변 품질 채점기

- **견고한 검증 (Robust Validation)**
  - 시간 기반 교차 검증(Time-based CV)로 Leakage 차단, CV-LB 상관 추적

- **가드레일 (Guardrails)**
  - 근거 추적·검증, 불충분 시 안전한 대체 답변(“근거 부족”) 출력

---

## 4. 작전 규범 (Operational Codex)

- **리포지토리 경계**: 모든 작업은 `nebula-con` 리포지토리 내부에서만 수행. 워크스페이스 루트 오염 금지
- **자동화**: Makefile / GitHub Actions 로 실험·배포 전 과정 자동화 및 재현성 보장
- **실험 관리**: Experiment Registry에 run_id/피처 해시/모델 파라미터/CV 기록 → 전 시도 추적
- **브랜치 전략**: `feat/*` 기능, `fix/*` 수정. PR을 통해서만 `main` 병합. PR 생성·검증은 아테나가 보좌

---

## 5. 즉시 실행 계획 (Immediate Action Plan)

1) **환경 분석**
   - 커서AI를 통해 `nebula-con`의 현재 상태(디렉토리, 의존성, 실행 경로) 점검 및 보고

2) **CI/CD 설계**
   - 코드 품질 자동 검사용 1차 GitHub Actions 워크플로우(`.github/workflows/ci.yml`) 설계 및 제안

3) **CI/CD 활성화**
   - 제안 워크플로우를 `nebula-con`에 추가, 최초 자동화 파이프라인 가동

---

## 6. 실행 우선순위 및 금지 사항 (Priority & Freeze)

- **최우선 목표**: Kaggle 대회 1위. 해당 목표 달성 관련 작업만 허용
- **작업 동결**: 본 SOP 외 모든 신규/부가 작업 중지. 변경은 PR로 SOP 개정 후 진행
- **품질 게이트**: CI 녹색 유지(테스트/린트/커버리지/임계치). 실패 시 병합 금지

---

## 7. 변경 관리 (Change Management)

- **문서 관리**: 본 문서가 Single Source of Truth. 개정 시 버전 및 변경 이력 명시
- **검토 절차**: 아테나 제안 → 사령관 승인 → 실행 유닛 적용 → CI 통과 → PR 병합

---

## 8. 부록 (산출물 체크리스트)

- 최소 실행(Tier 0) 산출물: `metrics/axes_run.json`, `metrics/profile.json`, `data/baseline_run.json`
- CI 아티팩트: 테스트/커버리지 리포트, 메트릭 JSON 검증 결과
- 문서화: Quick Start, Metrics Schema, Thresholds, Repro Guide (SOP 우선 이후 단계적으로 활성화) 