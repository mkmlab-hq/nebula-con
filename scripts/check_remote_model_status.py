#!/usr/bin/env python3
"""
Remote Model 상태 및 Connection 설정 확인
"""

from google.cloud import bigquery, bigquery_connection_v1


def check_remote_model_status():
    """Remote Model 상태 및 Connection 설정 확인"""
    print("🔍 Remote Model 상태 및 Connection 설정 확인...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 데이터셋 및 모델 목록 확인
        print("\n2️⃣ 데이터셋 및 모델 목록 확인...")
        dataset_id = f"{project_id}.nebula_con_kaggle"

        try:
            # 데이터셋 정보 확인
            dataset = client.get_dataset(dataset_id)
            print(f"   ✅ 데이터셋 존재: {dataset_id}")
            print(f"      위치: {dataset.location}")
            print(f"      생성 시간: {dataset.created}")

            # 데이터셋 내 테이블/모델 목록 확인
            tables = list(client.list_tables(dataset_id))
            print(f"   📊 데이터셋 내 객체 수: {len(tables)}")

            for table in tables:
                print(f"      - {table.table_id} ({table.table_type})")

        except Exception as e:
            print(f"   ❌ 데이터셋 확인 실패: {str(e)[:100]}...")

        # 3. Connection 상태 확인
        print("\n3️⃣ BigQuery Connection 상태 확인...")

        try:
            connection_client = bigquery_connection_v1.ConnectionServiceClient()
            connection_path = f"projects/{project_id}/locations/us-central1/connections/my_vertex_ai_connection"

            connection_info = connection_client.get_connection(name=connection_path)
            print(f"   ✅ Connection 존재: {connection_info.name}")
            print(f"      상태: {connection_info.state}")

            if connection_info.cloud_resource.service_account_id:
                print(
                    f"      서비스 계정: {connection_info.cloud_resource.service_account_id}"
                )

        except Exception as e:
            print(f"   ❌ Connection 확인 실패: {str(e)[:100]}...")

        # 4. 간단한 쿼리로 모델 존재 확인
        print("\n4️⃣ 모델 존재 확인 쿼리...")

        check_query = f"""
        SELECT 
          table_id,
          table_type,
          creation_time
        FROM `{dataset_id}.__TABLES__`
        WHERE table_id = 'text_embedding_remote_model'
        """

        try:
            query_job = client.query(check_query)
            results = query_job.result()

            for row in results:
                print(f"   ✅ 모델 확인됨: {row.table_id}")
                print(f"      타입: {row.table_type}")
                print(f"      생성 시간: {row.creation_time}")
                break
            else:
                print("   ❌ 모델을 찾을 수 없음")

        except Exception as e:
            print(f"   ❌ 모델 확인 쿼리 실패: {str(e)[:100]}...")

        # 5. 문제 진단
        print("\n5️⃣ 문제 진단...")
        print("   📋 가능한 원인:")
        print("   1. Remote Model이 실제로 생성되지 않음")
        print("   2. 모델 이름이 다름")
        print("   3. Connection 설정에 문제")
        print("   4. BigQuery ML 버전 문제")

        return True

    except Exception as e:
        print(f"\n❌ 확인 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    check_remote_model_status()
