-- text_embedding_remote_model 생성 SQL
-- BigQuery 콘솔에서 실행하여 원격 모델을 생성합니다.

CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`
REMOTE WITH CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
  endpoint = 'text-embedding-004' -- 최신 권장 모델 (textembedding-gecko@001 대신)
);

-- 모델 생성 후 확인 쿼리
SELECT 
  model_id, 
  model_type, 
  creation_time,
  options
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_id = 'text_embedding_remote_model'; 