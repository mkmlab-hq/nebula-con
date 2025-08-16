from google.cloud import bigquery
from google.oauth2 import service_account

# --- Parameters ---
PROJECT_ID = "persona-diary-service"
DATASET = "nebula_con_kaggle"
MODEL_NAME = "text_embedding_remote_model"
TABLE_NAME = "question_embeddings"
KEY_PATH = "/workspaces/nebula-con/gcs-key.json"  # 실제 서비스 계정 키 경로로 수정

# Create credentials
creds = service_account.Credentials.from_service_account_file(KEY_PATH)

# Initialize BigQuery client with credentials
client = bigquery.Client(credentials=creds, project=PROJECT_ID)

# Define your SQL query with 백틱
sql = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{TABLE_NAME}` AS
SELECT
  id,
  title,
  text,
  ML.GENERATE_EMBEDDING(
    MODEL `{PROJECT_ID}.{DATASET}.{MODEL_NAME}`,
    STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
  ) AS embedding
FROM
  `bigquery-public-data.hacker_news.full`
WHERE
  title IS NOT NULL OR text IS NOT NULL
LIMIT 10;
"""

print("Executing BigQuery job...")
try:
    # Start the query job and wait for it to complete
    query_job = client.query(sql)
    query_job.result()  # Wait for the job to finish
    print("✅ BigQuery job completed successfully.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
