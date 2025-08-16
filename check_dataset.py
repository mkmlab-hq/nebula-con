# check_dataset.py
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# GOOGLE_APPLICATION_CREDENTIALS 환경 변수가 설정되어 있어야 합니다.
# (이전 단계에서 이미 설정했습니다.)
client = bigquery.Client()
dataset_id = "persona-diary-service.nebula_con_kaggle"

try:
    dataset = client.get_dataset(dataset_id)
    print(f"✅ SUCCESS: Dataset '{dataset.dataset_id}' found in project '{dataset.project}'.")
    print("This confirms the dataset exists and you have at least viewer permissions.")
except NotFound:
    print(f"❌ FAILURE: Dataset '{dataset_id}' was NOT FOUND.")
    print("This means either the dataset does not exist, or your service account does not have permission to even see it.")
except Exception as e:
    print(f"❌ FAILURE: An unexpected error occurred: {e}") 