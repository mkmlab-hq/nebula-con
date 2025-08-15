#!/usr/bin/env python3
"""
Kaggle BigQuery AI 모델 접근 테스트 스크립트
"""

import sys
from google.cloud import bigquery
from google.auth import default


def test_kaggle_bigquery_access():
    """Kaggle BigQuery AI 모델 접근 테스트"""
    print("🔍 Kaggle BigQuery AI 모델 접근 테스트 시작...")

    try:
        # 1. 인증 정보 확인
        print("\n1️⃣ 인증 정보 확인 중...")
        credentials, project = default()
        print(f"   프로젝트: {project}")
        account_info = (
            credentials.service_account_email
            if hasattr(credentials, "service_account_email")
            else "User Account"
        )
        print(f"   계정: {account_info}")

        # 2. BigQuery 클라이언트 생성
        print("\n2️⃣ BigQuery 클라이언트 생성 중...")
        client = bigquery.Client(project=project)
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 3. Kaggle 데이터셋 접근 테스트
        print("\n3️⃣ Kaggle BigQuery AI 모델 데이터셋 접근 테스트...")

        # 테스트할 데이터셋들
        test_datasets = [
            "bigquery-public-data.kaggle_hackathons.bigquery_ai_models",
            "bigquery-public-data.kaggle_hackathons.bigquery_ai_models_v2",
            "bigquery-public-data.kaggle_hackathons.bigquery_ai_models_v3",
        ]

        for dataset in test_datasets:
            try:
                print(f"   🔍 {dataset} 접근 시도...")
                query = f"SELECT COUNT(*) as count FROM `{dataset}` LIMIT 1"
                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    print(f"      ✅ 접근 성공! 행 수: {row.count}")
                    break

            except Exception as e:
                print(f"      ❌ 접근 실패: {str(e)[:100]}...")

        # 4. 사용 가능한 데이터셋 검색
        print("\n4️⃣ 사용 가능한 Kaggle 관련 데이터셋 검색 중...")
        try:
            query = """
            SELECT 
                table_catalog,
                table_schema,
                table_name,
                table_type
            FROM `bigquery-public-data.kaggle_hackathons.INFORMATION_SCHEMA.TABLES`
            LIMIT 10
            """
            query_job = client.query(query)
            results = query_job.result()

            print("   📊 사용 가능한 테이블:")
            for row in results:
                print(f"      - {row.table_schema}.{row.table_name} ({row.table_type})")

        except Exception as e:
            print(f"   ❌ 스키마 정보 접근 실패: {str(e)[:100]}...")

        print("\n✅ 테스트 완료!")

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False

    return True


if __name__ == "__main__":
    success = test_kaggle_bigquery_access()
    sys.exit(0 if success else 1)
