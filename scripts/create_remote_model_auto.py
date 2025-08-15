#!/usr/bin/env python3
"""
Python으로 Remote Model 자동 생성
"""

from google.cloud import bigquery


def create_remote_model():
    """Remote Model 자동 생성"""
    print("🔧 Python으로 Remote Model 자동 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 데이터셋 생성
        print("\n2️⃣ 데이터셋 생성...")
        dataset_id = f"{project_id}.nebula_con_kaggle"

        try:
            dataset = client.get_dataset(dataset_id)
            print(f"   ✅ 데이터셋 이미 존재: {dataset_id}")
        except Exception:
            # 데이터셋이 없으면 생성
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "us-central1"
            dataset = client.create_dataset(dataset, timeout=30)
            print(f"   ✅ 데이터셋 생성 완료: {dataset_id}")

        # 3. Remote Model 생성
        print("\n3️⃣ Remote Model 생성 중...")

        create_model_sql = f"""
        CREATE OR REPLACE MODEL `{dataset_id}.text_embedding_remote_model`
        REMOTE WITH CONNECTION `{project_id}.us-central1.my_vertex_ai_connection`
        OPTIONS (
          remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
          endpoint = 'text-embedding-004'
        )
        """

        print("   🔍 실행할 SQL:")
        print(f"   {create_model_sql.strip()}")

        # SQL 실행
        query_job = client.query(create_model_sql)
        query_job.result()  # 완료까지 대기

        print("   ✅ Remote Model 생성 완료!")

        # 4. 모델 생성 확인
        print("\n4️⃣ 모델 생성 확인...")

        check_sql = f"""
        SELECT 
          table_id,
          creation_time,
          last_modified_time
        FROM `{dataset_id}.__TABLES__`
        WHERE table_id LIKE '%text_embedding%'
        """

        query_job = client.query(check_sql)
        results = query_job.result()

        for row in results:
            print(f"   ✅ 모델 확인됨: {row.table_id}")
            print(f"      생성 시간: {row.creation_time}")
            print(f"      수정 시간: {row.last_modified_time}")
            break

        print("\n🎉 Remote Model 생성 완료!")
        print(f"   📍 모델 경로: {dataset_id}.text_embedding_remote_model")
        print("\n   📋 다음 단계:")
        print("   1. ML.GENERATE_EMBEDDING 테스트 실행")
        print("   2. 캐글 해커톤 데이터에 적용")

        return True

    except Exception as e:
        print(f"\n❌ Remote Model 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    create_remote_model()
