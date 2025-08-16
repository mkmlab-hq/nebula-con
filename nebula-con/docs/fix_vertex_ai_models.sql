-- SCI 프리미엄 AI가 제시한 정확한 해결책
-- Vertex AI 엔드포인트에 연결되는 올바른 원격 모델 생성

-- 1단계: 기존 잘못된 모델 삭제 (필요시)
-- DROP MODEL IF EXISTS `persona-diary-service.nebula_con_kaggle.text_embedding_model`;
-- DROP MODEL IF EXISTS `persona-diary-service.nebula_con_kaggle.text_generation_model`;

-- 2단계: 올바른 서비스 유형으로 임베딩 모델 생성
CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_model`
REMOTE WITH CONNECTION `persona-diary-service.us-central1.us_vertex_ai_connect`
OPTIONS (ENDPOINT = 'text-embedding-004');

-- 3단계: 텍스트 생성을 위한 모델 생성
CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_generation_model`
REMOTE WITH CONNECTION `persona-diary-service.us-central1.us_vertex_ai_connect`
OPTIONS (ENDPOINT = 'gemini-1.5-flash-001');

-- 4단계: 모델 생성 상태 확인
SELECT 
  model_id,
  model_type,
  remote_service_type,
  endpoint,
  creation_time,
  last_modified_time
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_id IN ('text_embedding_model', 'text_generation_model');

-- 5단계: 연결 상태 확인
SELECT 
  connection_id,
  connection_type,
  remote_service_type,
  endpoint,
  status
FROM `persona-diary-service.us-central1.INFORMATION_SCHEMA.CONNECTIONS`
WHERE connection_id = 'us_vertex_ai_connect';

-- 6단계: 모델 테스트 (임베딩)
-- 아래 쿼리로 임베딩 모델이 정상 작동하는지 확인
/*
SELECT ml_generate_embedding_result
FROM ML.GENERATE_EMBEDDING(
  MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_model`,
  (SELECT 'test text for embedding' AS content)
);
*/

-- 7단계: 모델 테스트 (텍스트 생성)
-- 아래 쿼리로 텍스트 생성 모델이 정상 작동하는지 확인
/*
SELECT ml_generate_text_result
FROM ML.GENERATE_TEXT(
  MODEL `persona-diary-service.nebula_con_kaggle.text_generation_model`,
  'What is machine learning?',
  STRUCT(0.7 AS temperature, 100 AS max_output_tokens)
);
*/

-- 주의사항:
-- 1. connection_id가 실제 존재하는 연결명과 일치하는지 확인
-- 2. endpoint 이름이 Vertex AI에서 지원하는 정확한 모델명인지 확인
-- 3. 프로젝트 ID와 데이터셋 ID가 실제 환경과 일치하는지 확인
-- 4. 모델 생성 후 테스트 쿼리를 실행하여 정상 작동 확인 