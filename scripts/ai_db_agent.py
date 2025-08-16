import sqlite3
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import List, Dict, Any, Optional

# --- SQLite Functions ---
def list_tables_sqlite(db_path: str) -> List[str]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def describe_table_sqlite(db_path: str, table_name: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [
        {"cid": row[0], "name": row[1], "type": row[2], "notnull": row[3], "default": row[4], "pk": row[5]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return columns

def execute_query_sqlite(db_path: str, query: str) -> List[tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# --- BigQuery Functions ---
def get_bq_client(key_path: str, project_id: str) -> bigquery.Client:
    creds = service_account.Credentials.from_service_account_file(key_path)
    return bigquery.Client(credentials=creds, project=project_id)

def list_tables_bq(client: bigquery.Client, dataset_id: str) -> List[str]:
    dataset_ref = client.dataset(dataset_id)
    tables = client.list_tables(dataset_ref)
    return [table.table_id for table in tables]

def describe_table_bq(client: bigquery.Client, dataset_id: str, table_id: str) -> List[Dict[str, Any]]:
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    return [{"name": schema.name, "type": schema.field_type, "mode": schema.mode} for schema in table.schema]

def execute_query_bq(client: bigquery.Client, query: str) -> List[Dict[str, Any]]:
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]

# Example usage (uncomment and fill in your paths/IDs to test)
# SQLITE_DB_PATH = 'example.db'
# print(list_tables_sqlite(SQLITE_DB_PATH))
# print(describe_table_sqlite(SQLITE_DB_PATH, 'my_table'))
# print(execute_query_sqlite(SQLITE_DB_PATH, 'SELECT * FROM my_table LIMIT 5'))

# BQ_KEY_PATH = '/workspaces/nebula-con/gcs-key.json'
# BQ_PROJECT_ID = 'persona-diary-service'
# BQ_DATASET_ID = 'nebula_con_kaggle'
# bq_client = get_bq_client(BQ_KEY_PATH, BQ_PROJECT_ID)
# print(list_tables_bq(bq_client, BQ_DATASET_ID))
# print(describe_table_bq(bq_client, BQ_DATASET_ID, 'question_embeddings'))
# print(execute_query_bq(bq_client, 'SELECT * FROM `persona-diary-service.nebula_con_kaggle.question_embeddings` LIMIT 5'))
