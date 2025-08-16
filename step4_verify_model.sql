-- 4단계: 모델 생성 확인
-- 모델 생성 완료 후 이 SQL을 실행하여 모델이 생성되었는지 확인하세요

SELECT 
  model_id, 
  model_type, 
  creation_time,
  options
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_id = 'text_embedding_remote_model'; 