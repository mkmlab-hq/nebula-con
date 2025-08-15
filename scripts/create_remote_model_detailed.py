#!/usr/bin/env python3
"""
자세한 모니터링과 오류 처리를 포함한 Remote Model 생성
"""

import time

from google.cloud import bigquery


def create_remote_model_detailed():
    """자세한 모니터링과 오류 처리를 포함한 Remote Model 생성"""
    print("🔧 자세한 모니터링과 오류 처리를 포함한 Remote Model 생성...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 데이터셋 확인 및 생성
        print("\n2️⃣ 데이터셋 확인 및 생성...")
        dataset_id = f"{project_id}.nebula_con_kaggle"

        try:
            dataset = client.get_dataset(dataset_id)
            print(f"   ✅ 데이터셋 존재: {dataset_id}")
            print(f"      위치: {dataset.location}")

            # 기존 테이블/모델 확인
            tables = list(client.list_tables(dataset_id))
            print(f"   📊 기존 객체 수: {len(tables)}")

            # 기존 모델 삭제 (있다면)
            for table in tables:
                if "text_embedding" in table.table_id:
                    print(f"   🗑️ 기존 모델 삭제: {table.table_id}")
                    client.delete_table(table.reference)
                    print("      ✅ 삭제 완료")

        except Exception as e:
            print(f"   ❌ 데이터셋 확인 실패: {str(e)[:100]}...")
            return False

        # 3. Remote Model 생성 (더 간단한 구문)
        print("\n3️⃣ Remote Model 생성 (간단한 구문)...")

        # 방법 1: 기본 구문
        create_model_sql1 = f"""
        CREATE MODEL `{dataset_id}.text_embedding_remote_model`
        REMOTE WITH CONNECTION `{project_id}.us-central1.my_vertex_ai_connection`
        OPTIONS (
          endpoint = 'text-embedding-004'
        )
        """

        print("   🔍 방법 1: 기본 구문")
        print("   실행할 SQL:")
        print(f"   {create_model_sql1.strip()}")

        try:
            query_job = client.query(create_model_sql1)
            print("   ⏳ 모델 생성 중... (잠시 대기)")

            # 진행 상황 모니터링
            for i in range(30):  # 최대 30초 대기
                try:
                    job = client.get_job(query_job.job_id)
                    if job.state == "DONE":
                        if job.errors:
                            print(f"   ❌ 모델 생성 실패: {job.errors}")
                            break
                        else:
                            print("   ✅ 모델 생성 완료!")
                            break
                    else:
                        print(f"   ⏳ 진행 중... ({job.state})")
                        time.sleep(1)
                except Exception:
                    print(f"   ⏳ 진행 상황 확인 중... ({i + 1}/30)")
                    time.sleep(1)

            # 결과 확인
            if job.state == "DONE" and not job.errors:
                print("   🎉 Remote Model 생성 성공!")

                # 모델 확인
                time.sleep(5)  # 모델 등록 대기
                tables = list(client.list_tables(dataset_id))
                print(f"   📊 생성 후 객체 수: {len(tables)}")

                for table in tables:
                    print(f"      - {table.table_id}")

                return True
            else:
                print("   ❌ 모델 생성 실패")
                return False

        except Exception as e:
            print(f"   ❌ 방법 1 실패: {str(e)[:100]}...")

            # 방법 2: 더 간단한 구문
            print("\n   🔍 방법 2: 더 간단한 구문")

            create_model_sql2 = f"""
            CREATE MODEL `{dataset_id}.text_embedding_remote_model`
            REMOTE WITH CONNECTION `{project_id}.us-central1.my_vertex_ai_connection`
            """

            print("   실행할 SQL:")
            print(f"   {create_model_sql2.strip()}")

            try:
                query_job = client.query(create_model_sql2)
                query_job.result()  # 완료까지 대기
                print("   ✅ 방법 2 성공!")
                return True

            except Exception as e2:
                print(f"   ❌ 방법 2도 실패: {str(e2)[:100]}...")
                return False

    except Exception as e:
        print(f"\n❌ Remote Model 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    create_remote_model_detailed()
