#!/usr/bin/env python3
"""
수정된 Remote Model 생성 스크립트 - OPTIONS 완전 포함
"""

from google.api_core.exceptions import BadRequest
from google.cloud import bigquery


def create_remote_model_fixed():
    """수정된 Remote Model 생성"""
    print("🔧 수정된 Remote Model 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 데이터셋 확인 및 생성
        print("\n2️⃣ 데이터셋 확인 및 생성...")
        dataset_id = "nebula_con_kaggle"
        dataset_ref = client.dataset(dataset_id)

        try:
            dataset = client.get_dataset(dataset_ref)
            print(f"   ✅ 데이터셋 {dataset_id} 이미 존재")
            print(f"      위치: {dataset.location}")
            print(f"      생성 시간: {dataset.created}")
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "us-central1"
            dataset = client.create_dataset(dataset)
            print(f"   ✅ 데이터셋 {dataset_id} 생성 완료")

        # 3. Remote Model 생성 (완전한 OPTIONS 포함)
        print("\n3️⃣ Remote Model 생성 (완전한 OPTIONS 포함)...")

        create_model_sql = f"""
        CREATE OR REPLACE MODEL `{project_id}.{dataset_id}.text_embedding_remote_model`
        REMOTE WITH CONNECTION `projects/907685055657/locations/us-central1/connections/my_vertex_ai_connection`
        OPTIONS (
          remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
          endpoint = 'text-embedding-004'
        )
        """

        print("   🔍 실행할 SQL:")
        print(f"   {create_model_sql.strip()}")

        try:
            job = client.query(create_model_sql)
            print("   ⏳ 모델 생성 중... (잠시 대기)")
            job.result()  # 쿼리 완료 대기

            print("   ✅ Remote Model 생성 성공!")
            print(f"   📍 모델 경로: {project_id}.{dataset_id}.text_embedding_remote_model")

            # 4. 모델 생성 확인
            print("\n4️⃣ 모델 생성 확인...")
            time.sleep(5)  # 모델 등록 대기

            models = list(client.list_models(dataset_id))
            if models:
                print(f"   📊 데이터셋 내 객체 수: {len(models)}")
                for model in models:
                    print(f"      - 모델: {model.model_id}")
                    print(f"        생성 시간: {model.created}")
            else:
                print("   ⚠️ 모델 목록에서 확인되지 않음 (테이블 목록에서 확인)")

                tables = list(client.list_tables(dataset_id))
                print(f"   📊 테이블 목록에서 확인: {len(tables)}")
                for table in tables:
                    print(f"      - {table.table_id} ({table.table_type})")

            return True

        except BadRequest as e:
            print(f"   ❌ BadRequest 오류: {e}")
            return False
        except Exception as e:
            print(f"   ❌ 기타 오류: {e}")
            return False

    except Exception as e:
        print(f"\n❌ Remote Model 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    import time

    create_remote_model_fixed()
