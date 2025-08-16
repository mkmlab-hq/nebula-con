from google.cloud import bigquery
from google.api_core import exceptions

# 1. BigQuery 클라이언트 초기화
client = bigquery.Client(project='persona-diary-service')
print("✅ BigQuery 클라이언트 생성 성공.")

# 2. 데이터셋 내 모델 목록 확인
try:
    print("\n🔍 데이터셋 'nebula_con_kaggle' 내 모델 목록을 확인합니다...")
    
    # 데이터셋 내 모델 목록 조회
    models_query = """
    SELECT 
        model_id,
        model_type,
        creation_time,
        last_modified_time
    FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
    ORDER BY creation_time DESC
    """
    
    print("⏳ 모델 목록을 조회합니다...")
    models_job = client.query(models_query)
    models_results = models_job.result()
    
    print("\n📋 사용 가능한 모델 목록:")
    model_count = 0
    for row in models_results:
        print(f"  - {row.model_id} (타입: {row.model_type})")
        model_count += 1
    
    if model_count == 0:
        print("  ❌ 사용 가능한 모델이 없습니다.")
        print("\n💡 해결 방법:")
        print("  1. Vertex AI 연결을 먼저 생성해야 합니다.")
        print("  2. 원격 모델을 생성해야 합니다.")
    else:
        print(f"\n✅ 총 {model_count}개의 모델을 찾았습니다.")
        
except exceptions.GoogleAPICallError as e:
    print(f"\n❌ BigQuery API 호출 오류: {e}")
    
    if "INFORMATION_SCHEMA.ML_MODELS" in str(e):
        print("\n🔍 문제 분석: ML_MODELS 스키마에 접근할 수 없습니다.")
        print("💡 이는 데이터셋이 존재하지 않거나 ML 기능이 활성화되지 않았음을 의미합니다.")
        
except Exception as e:
    print(f"\n❌ 알 수 없는 오류: {e}")

# 3. 데이터셋 존재 여부 확인
try:
    print("\n🔍 데이터셋 'nebula_con_kaggle' 존재 여부를 확인합니다...")
    
    dataset_ref = client.dataset('nebula_con_kaggle', project='persona-diary-service')
    dataset = client.get_dataset(dataset_ref)
    
    print(f"✅ 데이터셋 '{dataset.dataset_id}'가 존재합니다.")
    print(f"  - 생성 시간: {dataset.created}")
    print(f"  - 위치: {dataset.location}")
    
except exceptions.NotFound:
    print("❌ 데이터셋 'nebula_con_kaggle'이 존재하지 않습니다.")
    print("💡 먼저 데이터셋을 생성해야 합니다.")
    
except Exception as e:
    print(f"❌ 데이터셋 확인 중 오류: {e}") 