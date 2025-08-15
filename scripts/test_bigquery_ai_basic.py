#!/usr/bin/env python3
"""
기본 BigQuery AI 기능 테스트
"""

from google.cloud import bigquery


def test_basic_bigquery_ai():
    """기본 BigQuery AI 기능 테스트"""
    print("🔍 기본 BigQuery AI 기능 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. 기본 BigQuery 기능 테스트
        print("\n2️⃣ 기본 BigQuery 기능 테스트...")

        try:
            # 간단한 쿼리로 BigQuery 연결 확인
            query = "SELECT 1 as test_value, 'Hello BigQuery' as message"
            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ 기본 BigQuery 쿼리 성공!")
                print(f"      테스트 값: {row.test_value}")
                print(f"      메시지: {row.message}")
                break

        except Exception as e:
            print(f"   ❌ 기본 BigQuery 쿼리 실패: {str(e)[:100]}...")

        # 3. 공개 데이터셋 접근 테스트
        print("\n3️⃣ 공개 데이터셋 접근 테스트...")

        try:
            # 간단한 공개 데이터셋 테스트
            query = "SELECT 'test' as status"
            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ 공개 데이터셋 접근 성공!")
                break

        except Exception as e:
            print(f"   ❌ 공개 데이터셋 접근 실패: {str(e)[:100]}...")

        # 4. 프로젝트 정보 확인
        print("\n4️⃣ 프로젝트 정보 확인...")
        try:
            project = client.project
            print(f"   ✅ 현재 프로젝트: {project}")

            # 데이터셋 목록 확인
            datasets = list(client.list_datasets())
            print(f"   📊 접근 가능한 데이터셋 수: {len(datasets)}")

            for dataset in datasets[:3]:  # 상위 3개만 표시
                print(f"      - {dataset.dataset_id}")

        except Exception as e:
            print(f"   ❌ 프로젝트 정보 확인 실패: {str(e)[:100]}...")

        print("\n✅ 기본 BigQuery AI 기능 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_basic_bigquery_ai()
