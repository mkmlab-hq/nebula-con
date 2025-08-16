-- 3단계: 원격 모델 생성
-- Connection 생성 완료 후 이 SQL을 실행하세요

CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`
REMOTE WITH CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
  endpoint = 'text-embedding-004' -- 최신 권장 모델 (textembedding-gecko@001 대신)
); 