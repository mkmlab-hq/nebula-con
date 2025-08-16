from google.cloud import bigquery
from google.api_core import exceptions

# 1. BigQuery 클라이언트 초기화
# project 인자는 환경 변수가 없을 경우를 대비한 안전 장치입니다.
client = bigquery.Client(project='persona-diary-service')
print("✅ BigQuery 클라이언트 생성 성공.")

# 2. 실행할 최종 SQL 쿼리
sql_query = """
CREATE OR REPLACE TABLE 
`persona-diary-service.nebula_con_kaggle.hacker_news_embeddings` AS
WITH source_data AS (
  SELECT
    id,
    title,
    text
  FROM
    `bigquery-public-data.hacker_news.full`
  WHERE
    title IS NOT NULL OR text IS NOT NULL
  LIMIT 1000
)
SELECT
  id,
  title,
  text,
  ML.GENERATE_EMBEDDING(
    MODEL 
    `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
    STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
  ).ml_generate_embedding_result AS embedding
FROM
  source_data;
"""
print("✅ SQL 쿼리 준비 완료.")

# 3. 쿼리 실행 요청
try:
    print("⏳ BigQuery에 작업 요청을 전송합니다...")
    query_job = client.query(sql_query)

    print("⏳ 작업이 완료될 때까지 대기합니다. 몇 분 정도 소요될 수 있습니다...")
    query_job.result()  # 작업이 끝날 때까지 동기적으로 기다립니다.

    print("\n🎉 성공! 테이블 'hacker_news_embeddings'가 성공적으로 생성 또는 교체되었습니다.")

except exceptions.GoogleAPICallError as e:
    print("\n❌ 오류 발생: BigQuery API 호출에 실패했습니다.")
    print(f"오류 메시지: {e}")

except Exception as e:
    print("\n❌ 알 수 없는 오류가 발생했습니다.")
    print(f"오류 메시지: {e}") 