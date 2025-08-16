#!/usr/bin/env python3
"""
올바른 구문으로 ML.GENERATE_EMBEDDING 테스트
"""

from google.cloud import bigquery


def test_ml_generate_embedding():
    """올바른 구문으로 ML.GENERATE_EMBEDDING 테스트"""
    print("🔍 올바른 구문으로 ML.GENERATE_EMBEDDING 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. 올바른 구문으로 ML.GENERATE_EMBEDDING 테스트
        print("\n2️⃣ ML.GENERATE_EMBEDDING 테스트...")

        # 방법 1: ML.GENERATE_EMBEDDING 함수 사용
        query1 = """
        SELECT
          ML.GENERATE_EMBEDDING(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            STRUCT('Hello World, this is a test sentence for BigQuery AI!' AS content)
          ) AS embedding
        """

        print("   🔍 방법 1: ML.GENERATE_EMBEDDING 함수")
        print("   실행할 쿼리:")
        print(f"   {query1.strip()}")

        try:
            query_job = client.query(query1)
            results = query_job.result()

            for row in results:
                print("   ✅ ML.GENERATE_EMBEDDING 성공!")
                print("   📊 임베딩 생성됨")
                break

        except Exception as e:
            print(f"   ❌ 방법 1 실패: {str(e)[:100]}...")

            # 방법 2: ml_generate_embedding 함수 사용 (소문자)
            print("\n   🔍 방법 2: ml_generate_embedding 함수 (소문자)")

            query2 = """
            SELECT
              ml_generate_embedding(
                MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
                STRUCT('Hello World, this is a test sentence for BigQuery AI!' AS content)
              ) AS embedding
            """

            print("   실행할 쿼리:")
            print(f"   {query2.strip()}")

            try:
                query_job = client.query(query2)
                results = query_job.result()

                for row in results:
                    print("   ✅ ml_generate_embedding 성공!")
                    print("   📊 임베딩 생성됨")
                    break

            except Exception as e2:
                print(f"   ❌ 방법 2도 실패: {str(e2)[:100]}...")

                # 방법 3: 다른 구문 시도
                print("\n   🔍 방법 3: 다른 구문 시도")

                query3 = """
                SELECT
                  ML.GENERATE_EMBEDDING(
                    MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
                    'Hello World, this is a test sentence for BigQuery AI!'
                  ) AS embedding
                """

                print("   실행할 쿼리:")
                print(f"   {query3.strip()}")

                try:
                    query_job = client.query(query3)
                    results = query_job.result()

                    for row in results:
                        print("   ✅ 방법 3 성공!")
                        print("   📊 임베딩 생성됨")
                        break

                except Exception as e3:
                    print("   ❌ 모든 방법 실패")
                    print(f"   최종 오류: {str(e3)[:100]}...")
                    raise e3

        print("\n✅ ML.GENERATE_EMBEDDING 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_ml_generate_embedding()
