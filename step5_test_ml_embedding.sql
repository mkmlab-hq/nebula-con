-- 5단계: ML.GENERATE_EMBEDDING 함수 테스트
-- 모든 단계 완료 후 이 SQL을 실행하여 ML 함수가 정상 작동하는지 확인하세요

-- 기본 테스트
SELECT ML.GENERATE_EMBEDDING(
  MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
  STRUCT('Hello, this is a test for Kaggle competition' AS content)
) AS embedding;

-- 해커뉴스 데이터로 실제 테스트
SELECT
  id,
  title,
  text,
  ML.GENERATE_EMBEDDING(
    MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
    STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
  ).ml_generate_embedding_result AS embedding
FROM
  `bigquery-public-data.hacker_news.full`
WHERE
  title IS NOT NULL OR text IS NOT NULL
LIMIT 5; 