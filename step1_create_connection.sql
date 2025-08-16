-- 1단계: Vertex AI Connection 생성
-- BigQuery 콘솔에서 이 SQL을 실행하세요

CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  connection_type = 'CLOUD_RESOURCE',
  resource_uri = '//aiplatform.googleapis.com/projects/persona-diary-service/locations/us-central1'
); 