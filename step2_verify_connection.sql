-- 2단계: Connection 생성 확인
-- BigQuery 콘솔에서 이 SQL을 실행하여 Connection이 생성되었는지 확인하세요

SELECT 
  connection_id, 
  connection_type, 
  properties
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
WHERE connection_id = 'my_vertex_ai_connection'; 