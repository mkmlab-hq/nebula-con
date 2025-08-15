#!/usr/bin/env python3
"""
ML.GENERATE_EMBEDDING 함수 테스트 - 정확한 오류 메시지 확인
"""

from google.cloud import bigquery


def test_ml_generate_embedding():
    """ML.GENERATE_EMBEDDING 함수 테스트"""
    print("🔍 ML.GENERATE_EMBEDDING 함수 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. ML.GENERATE_EMBEDDING 함수 테스트
        print("\n2️⃣ ML.GENERATE_EMBEDDING 함수 테스트...")

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

                print(f"      실행할 쿼리: {query.strip()}")

                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    print("      ✅ 모델 호출 성공! 임베딩 생성됨")
                    break

            except Exception as e:
                error_msg = str(e)
                print(f"      ❌ 오류 발생: {error_msg}")

                # 오류 타입별 분석
                if "403" in error_msg:
                    print("         → 403 Access Denied: 접근 권한 부족")
                elif "404" in error_msg:
                    print("         → 404 Not Found: 모델이 존재하지 않음")
                elif "400" in error_msg:
                    print(
                        "         → 400 Bad Request: 구문 오류 또는 잘못된 요청"
                    )
                elif "500" in error_msg:
                    print(
                        "         → 500 Internal Server Error: 서버 내부 오류"
                    )
                else:
                    print("         → 기타 오류")

        # 3. 다른 BigQuery AI 기능 테스트
        print("\n3️⃣ 다른 BigQuery AI 기능 테스트...")

        try:
            # ai.generate_text 함수 테스트 (소문자)
            query = """
            SELECT
              ai.generate_text(
                'Summarize this text: BigQuery AI provides powerful machine learning capabilities.',
                'gemini-pro'
              ) AS summary
            """

            print("   🔍 ai.generate_text 함수 테스트...")
            query_job = client.query(query)
            results = query_job.result()

            for row in results:
                print("   ✅ ai.generate_text 성공!")
                print(f"      요약: {row.summary[:200]}...")
                break

        except Exception as e:
            print(f"   ❌ ai.generate_text 실패: {str(e)[:100]}...")

        print("\n✅ ML.GENERATE_EMBEDDING 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_ml_generate_embedding()
