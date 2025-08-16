import textwrap
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# --- Parameter 설정 ---
PROJECT_ID = "persona-diary-service"
DATASET = "nebula_con_kaggle"
EMBEDDING_MODEL_NAME = "text_embedding_remote_model"
GENERATION_ENDPOINT = "gemini-1.0-pro"
CONNECTION_ID = "projects/persona-diary-service/locations/us/connections/vertex-conn-us-1"
KEY_PATH = "/workspaces/nebula-con/gcs-key.json"
TABLE_NAME_EMBEDDINGS = "hacker_news_embeddings"

creds = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=creds, project=PROJECT_ID)

def create_embeddings_table(limit=100):
    sql = textwrap.dedent(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{TABLE_NAME_EMBEDDINGS}` AS
    SELECT
      id,
      title,
      text,
      ML.GENERATE_EMBEDDING(
        MODEL `{PROJECT_ID}.{DATASET}.{EMBEDDING_MODEL_NAME}`,
        STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
      ) AS embedding
    FROM
      `bigquery-public-data.hacker_news.full`
    WHERE
      title IS NOT NULL OR text IS NOT NULL
    LIMIT {limit};
    """)
    print("Executing embedding generation query...")
    client.query(sql).result()
    print(f"✅ Embedding table '{TABLE_NAME_EMBEDDINGS}' created successfully with {limit} rows.")

def retrieve_and_generate(query_text: str, top_k: int = 3) -> str:
    # 1. 사용자 질문 임베딩 생성
  # 쿼리문을 한 줄로 단순화하고 print로 출력
  query_embedding_sql = (
    f"SELECT ML.GENERATE_EMBEDDING(MODEL `{PROJECT_ID}.{DATASET}.{EMBEDDING_MODEL_NAME}`, STRUCT('{query_text}' AS content)) AS embedding"
  )
  print("=== [BigQuery 쿼리문 최종 확인] ===")
  print(query_embedding_sql)
  query_job = client.query(query_embedding_sql)
  query_embedding = query_job.result().to_dataframe().iloc[0, 0]
  # query_embedding이 리스트/array라면 BigQuery 배열 리터럴로 변환
  if isinstance(query_embedding, (list, tuple)):
    embedding_literal = 'ARRAY[' + ', '.join([str(float(x)) for x in query_embedding]) + ']'
  else:
    embedding_literal = str(query_embedding)

    # 2. 코사인 유사도 기반 시맨틱 검색
    semantic_search_sql = textwrap.dedent(f"""
    SELECT
      text,
      title,
      ML.DISTANCE(embedding, {embedding_literal}, 'COSINE') as distance
    FROM
      `{PROJECT_ID}.{DATASET}.{TABLE_NAME_EMBEDDINGS}`
    ORDER BY
      distance
    LIMIT {top_k}
    """)
    search_job = client.query(semantic_search_sql)
    retrieved_docs_df = search_job.result().to_dataframe()

    docs_for_prompt = "\n".join([
        f"Title: {row.title}\nText: {row.text}" for _, row in retrieved_docs_df.iterrows()
    ])

    prompt = f"""
    Based on the following documents, answer the user's question.
    Do not use any external knowledge. If the documents do not contain the answer,
    state that you cannot find the answer in the provided documents.

    Documents:
    {docs_for_prompt}

    Question:
    {query_text}
    """

    generation_sql = textwrap.dedent(f"""
    SELECT
      AI.GENERATE(
        ('Summarize the following Stack Overflow question in one short sentence: ', '{prompt}'),
        connection_id => '{CONNECTION_ID}',
        endpoint => '{GENERATION_ENDPOINT}'
      ).result AS summary
    """)
    generation_job = client.query(generation_sql)
    response_text = generation_job.result().to_dataframe().iloc[0, 0]

    return response_text

# --- RAG 파이프라인 실행 예시 ---
if __name__ == "__main__":
    # 임베딩 테이블이 없다면 먼저 생성 (최초 1회만)
    # create_embeddings_table(limit=100)
    user_question = "What is the news about AI?"
    answer = retrieve_and_generate(user_question)
    print("\n" + "="*50)
    print(f"User Question: {user_question}")
    print("-"*50)
    print(f"AI-generated Answer:\n{answer}")
    print("="*50)
