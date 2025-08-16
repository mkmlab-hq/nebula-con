### rPPG+음성 통합 건강도 시스템 기술 구현 문서 (Hephaestus 2.1)

## 1. 개요
- 목표: Robust/Reliable/Verifiable/Evolvable rPPG 기반 시스템으로 고도화하고, 음성 분석 모듈을 결합한 멀티모달 건강도 평가를 상용화 준비 수준으로 구현
- 핵심 성과 목표
  - HR 정확도: UBFC-rPPG 기준 MAE ≤ 3.5 BPM
  - 실시간: 640×480 ≥ 20 FPS, WebSocket 1 Hz 결과 송신, E2E < 300 ms
  - 재현성: AE/AWB Lock + SQI 게이팅 + 반복 측정 표준편차 ≤ 5 BPM
  - 진화성: 저SQI 세션 자동 축적 → 주기적 재학습 → 벤치마크 자동 비교(≥5% 개선)

## 2. 시스템 아키텍처
- 파이프라인: 카메라 → 얼굴 감지/추적(폴백) → ROI 추출/안정화 → 신호처리(POS/CHROM/ICA) → 품질가중 융합 → HR 추정(추적/클램프) → SQI 게이팅 → 바이탈/건강도 → WebSocket 출력
- 음성 경로(병렬): 마이크 → VAD → 음향특징 → 스트레스/정서 → 모달 융합(품질 기반)
- 디렉터리/파일
  - `src/face/detectors.py`(신규): FaceMesh/YuNet/Haar 라우팅
  - `src/face/roi_stabilizer.py`(신규): ROI EMA 안정화
  - `real_rppg_analysis.py`: POS/CHROM/ICA + 품질가중 융합
  - `src/signal/hr_tracker.py`(신규): EMA/1D 칼만 + 점프 클램프
  - `src/signal/quality.py`(신규): SQI 계산·게이팅·가이드 사유
  - `real_biometric_analyzer.py`: 카메라 AE/AWB Lock/프리셋
  - `api/ws.py`(신규): Secure WebSocket(wss) + JWT 인증
  - `scripts/benchmark_ubfc.py`(신규): 벤치마크/리포트
  - `scripts/retrain_model.py`(신규): 데이터 선순환 재학습
  - `config/vision.yaml`, `config/signal.yaml`, `config/runtime.yaml`(신규)

## 3. Phase 1 — 신호 무결성 및 정확도
### 3.1 ROI 추출기 교체(폴백 라우터 + 안정화)
- 기본: MediaPipe FaceMesh → 폴백: YuNet(OpenCV DNN, FP16) → Haar
- 안정화: ROI 중심/면적 EMA(α≈0.6), 5–10프레임 간헐 재검출
- 성능: 폭 640 다운스케일, ROI만 색공간 변환, 스레딩/큐 처리

### 3.2 고급 신호처리 및 품질가중 융합
- 알고리즘: POS, CHROM, ICA(3성분→심박대역 에너지비로 성분 선택)
- 윈도우: 10–12 s, 50% 오버랩
- 품질가중: 각 신호의 SNR(dB)·피크 prominence 정규화 → 가중 합(quality-aware fusion)

### 3.3 HR 추적 고도화
- 전처리: detrend + Butterworth bandpass(0.7–4.0 Hz, sos)
- 피크: `find_peaks(prominence=…)` 신뢰도 산출
- 추적: EMA 기본(+가속도 클램프), 필요 시 1D 칼만; 초당 ±5 BPM 이상 변화 클램핑

## 4. Phase 2 — 신뢰성·사용자 경험
### 4.1 SQI 도입·출력 게이팅
- SQI = SNR_norm(0.35) + ACF_peak(0.25) + ROI 안정도(0.20) + (1−모션_norm)(0.20)
- 임계치: SQI<0.6 → 결과 홀드 + 재측정 가이드(사유 코드 포함)

### 4.2 카메라 제어 + 환경 가이드
- AE/AWB Lock 옵션(CAP_DSHOW 우선), 실패 시 폴백/로그
- 노출/화이트밸런스 프리셋(밝은/어두운), FPS 고정(≥30)
- UI: 실시간 SQI 서브컴포넌트 기반 맞춤 메시지

## 5. Phase 3 — 서비스화·검증
### 5.1 Secure WebSocket(1 Hz) + JWT
- 엔드포인트: `wss://…/ws/metrics`
- 페이로드 예시:
```json
{"hr":72.3,"hrv":42.1,"rr":14.8,"bp":[118,76],"sqi":0.82,"snr":9.7,"ts":1720422334.12,"confidence":{"hr":0.84,"bp":0.42}}
```
- 백프레셔/레이트리밋: 큐 최대 길이, 최신값 우선, 1 Hz flush

### 5.2 공식 벤치마크 자동화
- 입력: UBFC-rPPG(피험자 분리)
- 비교: Green-Baseline vs Fusion Engine
- 산출: HR MAE/RMSE/ρ, Bland–Altman, SNR/가용률, 처리시간
- 재현성: 리포트에 Git commit/tag/의존성 버전 기록

### 5.3 BP(연구용) 운영정책
- 디폴트 비노출; 개인 1–2점 보정·SQI≥0.7 시 제한 표시
- 상시 디스클레이머(“연구용 참고 수치”), 신뢰도·오차범위 동반

## 6. Phase 4 — 운영·지속적 개선
### 6.1 데이터 선순환
- 실패 세션(GCS `mkm-lab-retraining-data`): 저SQI 클립(+SQI 메타) 자동 업로드
- 재학습: 주기적 파인튜닝 → 벤치마크 자동 비교(이전 대비 MAE ≥5% 개선) 시 롤아웃

### 6.2 고급 관측성
- 구조화 로깅(JSON, `trace_id`, `session_id`, `model_version`)
- 프로메테우스 메트릭: 평균 SQI, 측정 성공률, 아웃라이어 비율, FPS, WS 지연
- Grafana 대시보드: 비즈니스/품질/성능 지표 가시화

## 7. 멀티모달 통합(얼굴 rPPG + 음성)
### 7.1 음성 분석 모듈
- 입력: 16 kHz PCM, WebRTC VAD
- 특징: MFCC/스펙트럴/폼란트/피치/지터·쉬머(가능시)
- 산출: 스트레스/각성(0–1), 감정 벡터, 발화 품질(신뢰도)

### 7.2 통합 전략
- `BioSignalsEngine`: `FaceVitalModule`(rPPG), `VoiceStressModule`(음성), `FusionModule`
- 시간정렬: UTC 타임스탬프 기반 1 s 버킷
- 품질가중 융합: rPPG(SQI), 음성(VAD 신뢰도·SNR·발화 커버리지) 가중 평균
- 폴백: Face SQI<0.6 → 음성 우선; 둘 다 불량 → “측정 불가”

### 7.3 통합 출력 스키마(WS)
```json
{
  "hr":72.3, "hr_conf":0.84,
  "rr":14.8, "rr_conf":0.77,
  "stress_mm":0.62, "stress_face":0.58, "stress_voice":0.66,
  "sqi_face":0.82, "q_voice":0.80,
  "ts":1720422334.12, "model_version":"rppg-2.1.0+voice-1.3.2"
}
```

## 8. 내부 API·설정·보안
### 8.1 내부 API(파이썬)
- `RobustFaceDetector.detect(frame) -> ROI`
- `ROIStabilizer.update(roi) -> roi_stable`
- `SignalEngine.process(roi_series) -> {pos, chrom, ica, snr, prom}`
- `HRTracker.update(peak|spectrum) -> hr, conf`
- `SQI.compute(features) -> score, reasons[]`

### 8.2 설정 샘플(`config/signal.yaml`)
```yaml
window_sec: 10
overlap: 0.5
bandpass_hz: [0.7, 4.0]
fusion_weights: {snr: 0.6, peak_conf: 0.4}
sqi_threshold: 0.6
hr_tracking: {method: ema, alpha: 0.35, clamp_bpm_per_sec: 5}
```

### 8.3 보안
- WS: `wss://` + JWT(만료/서명키 회전), IP 제한(옵션), PII 최소화, 전송·저장 암호화
- 버전 핀: `mediapipe`, `numpy`, `protobuf`, `opencv-python`, `scipy` 호환 버전 고정

## 9. 테스트·검증·배포
### 9.1 테스트
- 단위: 검출 폴백/ROI 안정화/필터/피크/추적/SQI/WS
- 통합: 카메라→WS→프론트, 저조도/모션/가림 시나리오
- 벤치마크: UBFC-rPPG 자동 리포트(표/그림/로그/커밋)

### 9.2 배포
- Docker(CUDA 베이스), `.env`/`config/*.yaml` 환경 분리
- 런북: 드라이버/카메라 권한/포트/WSS 인증서 로테이션

## 10. 일정(권장)
- 주 1: ROI 라우터+EMA, AE/AWB Lock, POS/CHROM/ICA, HR 추적
- 주 2: SQI·게이팅·가이드, wss+JWT, UBFC 벤치마크, 관측성, 음성 연동 최소기
- 이후: 데이터 선순환·재학습, 대시보드 고도화

## 11. 수용 기준(요약)
- HR: MAE ≤ 3.5 BPM, 인접 1 s 변동 ≤ 10 BPM(95%)
- 실시간: 640×480 ≥ 20 FPS, WS E2E < 300 ms
- 재현성: 반복 표준편차 ≤ 5 BPM
- 벤치마크/재현성: 자동 리포트 + 모델 버전 기록
- 운영: 평균 SQI/성공률 대시보드 가동
- BP: 연구용 표기·게이팅·보정 워크플로우

## 12. SQI→가이드 매핑(예)
- SNR 낮음: “조명이 약합니다. 밝은 곳에서 다시 시도하세요.”
- 모션 높음: “머리를 고정하고 10초간 움직임을 줄여주세요.”
- ROI 불안정: “얼굴이 프레임 중앙을 벗어났습니다. 중앙에 맞춰주세요.”

## 13. 음성 가이드(보조)
- VAD 미검출: “마이크에 가깝게 평소처럼 5초간 말해보세요.”
- 잡음 높음: “조용한 환경에서 다시 시도하세요.”

