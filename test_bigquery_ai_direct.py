#!/usr/bin/env python3
"""
BigQuery AI 모델 직접 접근 테스트
"""

from google.cloud import bigquery


def test_bigquery_ai_direct():
    """BigQuery AI 모델 직접 접근 테스트"""
    print("🔍 BigQuery AI 모델 직접 접근 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. textembedding-gecko@001 모델 직접 호출 테스트
        print("\n2️⃣ textembedding-gecko@001 모델 직접 호출 테스트...")

        # 테스트할 모델들
        test_models = [
            "bigquery-public-data.ml_models.textembedding_gecko@001",
            "bigquery-public-data.ml_models.textembedding_gecko@002",
            "bigquery-public-data.ml_models.textembedding_gecko@003",
        ]

        for model in test_models:
            try:
                print(f"   🔍 {model} 모델 테스트...")

                # ML.GENERATE_EMBEDDING 함수 호출
                query = f"""
                SELECT
                  ML.GENERATE_EMBEDDING(
                    MODEL `{model}`,
                    STRUCT('Hello World' AS content)
                  ) AS embedding
                LIMIT 1
                """

                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    print("      ✅ 모델 호출 성공! 임베딩 생성됨")
                    break

            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg:
                    print("      ❌ 403 Access Denied: 조직 정책으로 인한 접근 제한")
                elif "404" in error_msg:
                    print("      ❌ 404 Not Found: 모델이 존재하지 않음")
                else:
                    print(f"      ❌ 오류: {error_msg[:100]}...")

        # 3. 다른 BigQuery AI 기능 테스트
        print("\n3️⃣ 다른 BigQuery AI 기능 테스트...")

        try:
            # AI.GENERATE_TEXT 함수 테스트
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
                print(f"   ✅ AI.GENERATE_TEXT 성공: {row.summary[:100]}...")
                break

        except Exception as e:
            print(f"   ❌ AI.GENERATE_TEXT 실패: {str(e)[:100]}...")

        print("\n✅ BigQuery AI 모델 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_bigquery_ai_direct()
