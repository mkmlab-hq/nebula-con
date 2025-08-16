-- Vertex AI Connection 생성 SQL
-- BigQuery 콘솔에서 실행하여 Connection을 생성합니다.

-- 1단계: Vertex AI Connection 생성
CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  connection_type = 'CLOUD_RESOURCE',
  resource_uri = '//aiplatform.googleapis.com/projects/persona-diary-service/locations/us-central1'
);

-- 2단계: Connection 생성 확인
SELECT 
  connection_id, 
  connection_type, 
  properties
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
WHERE connection_id = 'my_vertex_ai_connection';

-- 3단계: Connection 생성 후 원격 모델 생성
CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`
REMOTE WITH CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
  endpoint = 'text-embedding-004' -- 최신 권장 모델 (textembedding-gecko@001 대신)
);

-- 4단계: 모델 생성 확인
SELECT 
  model_id, 
  model_type, 
  creation_time,
  options
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_id = 'text_embedding_remote_model'; 