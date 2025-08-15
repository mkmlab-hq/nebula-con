-- BigQuery Remote Model 생성 SQL
-- 이 스크립트를 BigQuery 콘솔에서 실행하세요

-- 1. 데이터셋 생성 (없는 경우)
CREATE DATASET IF NOT EXISTS `persona-diary-service.nebula_con_kaggle`;

-- 2. Remote Model 생성
CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`
REMOTE WITH CONNECTION `persona-diary-service.us-central1.my_vertex_ai_connection`
OPTIONS (
  remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
  endpoint = 'text-embedding-004'  -- 최신 텍스트 임베딩 모델
);

-- 3. 모델 생성 확인
SELECT 
  model_id,
  model_type,
  creation_time,
  last_modified_time
FROM `persona-diary-service.nebula_con_kaggle.__TABLES__`
WHERE table_id LIKE '%text_embedding%'; 