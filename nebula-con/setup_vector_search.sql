-- BigQuery VECTOR_SEARCH 설정을 위한 SQL 스크립트
-- Grok의 최종 해결책: 사전 임베딩 계산 + 벡터 인덱스 생성

-- 1단계: 사전 임베딩 계산 테이블 생성
-- NULL 값을 COALESCE로 처리하고 필터링하여 None 오류 완전 방지
CREATE OR REPLACE TABLE `persona-diary-service.your_dataset.hacker_news_with_emb` AS
SELECT
  id,
  title,
  text,
  CONCAT(COALESCE(title, ''), ' ', COALESCE(text, '')) AS combined_text,
  ml_generate_embedding_result AS embedding
FROM ML.GENERATE_EMBEDDING(
  MODEL `persona-diary-service.your_dataset.embedding_model`,
  (SELECT 
     id, 
     title, 
     text, 
     CONCAT(COALESCE(title, ''), ' ', COALESCE(text, '')) AS content
   FROM `persona-diary-service.your_dataset.hacker_news`
   WHERE text IS NOT NULL OR title IS NOT NULL)
)
WHERE ml_generate_embedding_status = '';

-- 2단계: 벡터 인덱스 생성 (빠른 코사인 기반 검색용)
-- IVF (Inverted File Index) 사용으로 대용량 데이터셋에서도 빠른 검색
CREATE OR REPLACE VECTOR INDEX hn_vector_index
ON `persona-diary-service.your_dataset.hacker_news_with_emb`(embedding)
OPTIONS (
  index_type = 'IVF', 
  distance_type = 'COSINE', 
  num_lists = 100  -- 데이터셋 크기에 따라 조정 (100-1000)
);

-- 3단계: 인덱스 상태 확인
-- 인덱스 생성 완료 후 검색 가능 여부 확인
SELECT 
  table_name,
  index_name,
  index_type,
  distance_type,
  num_lists,
  status
FROM `persona-diary-service.your_dataset.INFORMATION_SCHEMA.VECTOR_INDEXES`
WHERE table_name = 'hacker_news_with_emb';

-- 4단계: 임베딩 테이블 데이터 확인
-- 사전 계산된 임베딩이 정상적으로 생성되었는지 확인
SELECT 
  COUNT(*) as total_rows,
  COUNT(embedding) as rows_with_embeddings,
  COUNT(*) - COUNT(embedding) as rows_without_embeddings
FROM `persona-diary-service.your_dataset.hacker_news_with_emb`;

-- 5단계: 샘플 데이터 확인
-- 임베딩 벡터의 차원과 품질 확인
SELECT 
  id,
  title,
  text,
  ARRAY_LENGTH(embedding) as embedding_dimensions,
  embedding[OFFSET(0)] as first_dimension_sample
FROM `persona-diary-service.your_dataset.hacker_news_with_emb`
LIMIT 5;

-- 6단계: VECTOR_SEARCH 테스트 쿼리
-- 실제 검색이 작동하는지 테스트 (임베딩 모델이 준비된 후 실행)
-- 예시: "machine learning" 관련 문서 검색
/*
SELECT 
  base.id, 
  base.title, 
  base.text, 
  base.combined_text, 
  query.distance as cosine_distance,
  1 - query.distance as similarity_score
FROM VECTOR_SEARCH(
  TABLE `persona-diary-service.your_dataset.hacker_news_with_emb`,
  'embedding',
  (SELECT [0.1, 0.2, 0.3, ...] AS embedding),  -- 실제 쿼리 임베딩으로 대체
  top_k => 5,
  OPTIONS => '{ "fraction_lists_to_search": 0.05 }'
) AS query
ORDER BY similarity_score DESC;
*/

-- 주의사항:
-- 1. 'your_dataset'을 실제 데이터셋 ID로 변경
-- 2. 'hacker_news'를 실제 소스 테이블명으로 변경
-- 3. embedding_model이 사전에 생성되어 있어야 함
-- 4. 벡터 인덱스 생성은 시간이 걸릴 수 있음 (대용량 데이터의 경우)
-- 5. VECTOR_SEARCH 테스트는 인덱스 생성 완료 후 실행 