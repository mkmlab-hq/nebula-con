from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import os

# GCP 프로젝트 ID 설정 (환경 변수 또는 직접 지정)
PROJECT_ID = "persona-diary-service"  # 실제 GCP 프로젝트 ID로 변경

client = bigquery.Client(project=PROJECT_ID)

# 임베딩을 생성할 소스 테이블 및 컬럼
SOURCE_TABLE = "`bigquery-public-data.hacker_news.full`"
TEXT_COLUMN = "CONCAT(IFNULL(title, ''), ' ', IFNULL(text, ''))"  # title과 text 결합

# 생성된 원격 임베딩 모델
REMOTE_EMBEDDING_MODEL = "persona-diary-service.nebula_con_kaggle.text_embedding_remote_model"

# 결과를 저장할 대상 테이블
DESTINATION_TABLE = f"{PROJECT_ID}.nebula_con_kaggle.hacker_news_embeddings"

def generate_embeddings_for_hacker_news(limit: int = 10) -> None:
    """
    Hacker News 데이터셋에서 텍스트 임베딩을 생성하여 BigQuery 테이블에 저장합니다.
    """
    query = f"""
    CREATE OR REPLACE TABLE `{DESTINATION_TABLE}` AS
    SELECT
      id,
      title,
      text,
      ML.GENERATE_EMBEDDING(
        MODEL `{REMOTE_EMBEDDING_MODEL}`,
        STRUCT({TEXT_COLUMN} AS content)
      ) AS embedding
    FROM
      {SOURCE_TABLE}
    WHERE
      title IS NOT NULL OR text IS NOT NULL
    LIMIT {limit}
    """

    job_config = bigquery.QueryJobConfig(write_disposition='WRITE_TRUNCATE')

    print(f"🚀 Hacker News 임베딩 생성 시작 (제한: {limit}행)...")
    print(f"대상 테이블: {DESTINATION_TABLE}")

    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # 쿼리 실행 완료까지 대기
        print(f"✅ Hacker News 임베딩 생성 및 저장 완료: {DESTINATION_TABLE}")
    except Exception as e:
        print(f"❌ 임베딩 생성 실패: {e}")
        print("🔍 로그를 확인하여 문제를 파악하세요.")

if __name__ == "__main__":
    generate_embeddings_for_hacker_news(limit=10)  # 테스트를 위해 10개 행으로 제한
