#!/usr/bin/env python3
"""
BigQuery ML 공식 문서 기반 테스트
"""

from google.cloud import bigquery


def test_bigquery_ml_official():
    """BigQuery ML 공식 문서 기반 테스트"""
    print("🔍 BigQuery ML 공식 문서 기반 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. 다양한 BigQuery ML 구문 시도
        print("\n2️⃣ 다양한 BigQuery ML 구문 시도...")

        # 방법 1: 표준 ML.GENERATE_EMBEDDING
        print("   🔍 방법 1: 표준 ML.GENERATE_EMBEDDING")
        query1 = """
        SELECT
          ML.GENERATE_EMBEDDING(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            STRUCT('Hello World' AS content)
          ) AS embedding
        """

        try:
            query_job = client.query(query1)
            results = query_job.result()

            for row in results:
                print("   ✅ 방법 1 성공!")
                print("   📊 임베딩 생성됨")
                return True

        except Exception as e:
            print(f"   ❌ 방법 1 실패: {str(e)[:100]}...")

        # 방법 2: ml_generate_embedding (소문자)
        print("\n   🔍 방법 2: ml_generate_embedding (소문자)")
        query2 = """
        SELECT
          ml_generate_embedding(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            STRUCT('Hello World' AS content)
          ) AS embedding
        """

        try:
            query_job = client.query(query2)
            results = query_job.result()

            for row in results:
                print("   ✅ 방법 2 성공!")
                print("   📊 임베딩 생성됨")
                return True

        except Exception as e:
            print(f"   ❌ 방법 2 실패: {str(e)[:100]}...")

        # 방법 3: 간단한 문자열 전달
        print("\n   🔍 방법 3: 간단한 문자열 전달")
        query3 = """
        SELECT
          ML.GENERATE_EMBEDDING(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            'Hello World'
          ) AS embedding
        """

        try:
            query_job = client.query(query3)
            results = query_job.result()

            for row in results:
                print("   ✅ 방법 3 성공!")
                print("   📊 임베딩 생성됨")
                return True

        except Exception as e:
            print(f"   ❌ 방법 3 실패: {str(e)[:100]}...")

        # 방법 4: 다른 함수명 시도
        print("\n   🔍 방법 4: 다른 함수명 시도")
        query4 = """
        SELECT
          GENERATE_EMBEDDING(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            'Hello World'
          ) AS embedding
        """

        try:
            query_job = client.query(query4)
            results = query_job.result()

            for row in results:
                print("   ✅ 방법 4 성공!")
                print("   📊 임베딩 생성됨")
                return True

        except Exception as e:
            print(f"   ❌ 방법 4 실패: {str(e)[:100]}...")

        print("\n❌ 모든 방법 실패")
        print("   📋 문제 분석:")
        print("   1. Remote Model이 제대로 생성되지 않았을 수 있음")
        print("   2. BigQuery ML 구문이 변경되었을 수 있음")
        print("   3. Connection 설정에 문제가 있을 수 있음")

        return False

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_bigquery_ml_official()
