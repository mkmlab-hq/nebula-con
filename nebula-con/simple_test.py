from google.cloud import bigquery

client = bigquery.Client()
print("✅ BigQuery 클라이언트 생성 성공")

query = """
SELECT
  ML.GENERATE_EMBEDDING(
    MODEL `bigquery-public-data.ml_models.textembedding_gecko@001`,
    STRUCT('Hello World' AS content)
  ) AS embedding
LIMIT 1
"""

print("🔍 textembedding-gecko@001 모델 호출 시도...")
try:
    query_job = client.query(query)
    results = query_job.result()
    print("✅ 모델 호출 성공!")
except Exception as e:
    print(f"❌ 실패: {str(e)}")
