#!/usr/bin/env python3
"""
대안 BigQuery AI 기능 테스트 - 조직 정책 제한 우회
"""

from google.cloud import bigquery


def test_alternative_bigquery_ai():
    """조직 정책 제한을 우회하여 다른 BigQuery AI 기능 테스트"""
    print("🔍 대안 BigQuery AI 기능 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. AI.GENERATE_TEXT 함수 테스트 (Gemini Pro)
        print("\n2️⃣ AI.GENERATE_TEXT 함수 테스트 (Gemini Pro)...")
        try:
            query = """
            SELECT
              AI.GENERATE_TEXT(
                'Summarize this text: BigQuery AI provides powerful machine learning capabilities directly within SQL queries.',
                'gemini-pro'
              ) AS summary
            """

            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ AI.GENERATE_TEXT 성공!")
                print(f"      요약: {row.summary[:200]}...")
                break

        except Exception as e:
            print(f"   ❌ AI.GENERATE_TEXT 실패: {str(e)[:100]}...")

        # 3. AI.GENERATE_BOOL 함수 테스트
        print("\n3️⃣ AI.GENERATE_BOOL 함수 테스트...")
        try:
            query = """
            SELECT
              AI.GENERATE_BOOL(
                'Is the following statement true? BigQuery is a cloud data warehouse.',
                'gemini-pro'
              ) AS is_true
            """

            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ AI.GENERATE_BOOL 성공!")
                print(f"      결과: {row.is_true}")
                break

        except Exception as e:
            print(f"   ❌ AI.GENERATE_BOOL 실패: {str(e)[:100]}...")

        # 4. AI.GENERATE_TABLE 함수 테스트
        print("\n4️⃣ AI.GENERATE_TABLE 함수 테스트...")
        try:
            query = """
            SELECT
              AI.GENERATE_TABLE(
                'Create a table with 3 columns: Product Name, Price, Category. Fill with 2 sample rows.',
                'gemini-pro',
                STRUCT(
                  'Product Name' AS column_name,
                  'STRING' AS data_type
                ),
                STRUCT(
                  'Price' AS column_name,
                  'FLOAT64' AS data_type
                ),
                STRUCT(
                  'Category' AS column_name,
                  'STRING' AS data_type
                )
              ) AS generated_table
            """

            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ AI.GENERATE_TABLE 성공!")
                print(f"      생성된 테이블: {row.generated_table}")
                break

        except Exception as e:
            print(f"   ❌ AI.GENERATE_TABLE 실패: {str(e)[:100]}...")

        # 5. 공개 BigQuery 데이터셋 활용 테스트
        print("\n5️⃣ 공개 BigQuery 데이터셋 활용 테스트...")
        try:
            query = """
            SELECT
              name,
              population,
              AI.GENERATE_TEXT(
                CONCAT('Describe this city: ', name, ' with population ', population),
                'gemini-pro'
              ) AS description
            FROM `bigquery-public-data.utility_us.city`
            WHERE population > 1000000
            LIMIT 3
            """

            query_job = client.query(query)
            results = query_job.result()

            print("   ✅ 공개 데이터셋 + AI.GENERATE_TEXT 성공!")
            for row in results:
                print(f"      도시: {row.name}, 인구: {row.population:,}")
                print(f"      설명: {row.description[:100]}...")
                print()

        except Exception as e:
            print(f"   ❌ 공개 데이터셋 테스트 실패: {str(e)[:100]}...")

        print("\n✅ 대안 BigQuery AI 기능 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_alternative_bigquery_ai()
