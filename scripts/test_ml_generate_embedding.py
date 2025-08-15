#!/usr/bin/env python3
"""
Remote Model을 사용한 ML.GENERATE_EMBEDDING 테스트
"""

from google.cloud import bigquery


def test_ml_generate_embedding():
    """Remote Model을 사용한 ML.GENERATE_EMBEDDING 테스트"""
    print("🔍 Remote Model을 사용한 ML.GENERATE_EMBEDDING 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        print("   ✅ BigQuery 클라이언트 생성 성공")

        # 2. Remote Model을 사용한 임베딩 생성 테스트
        print("\n2️⃣ ML.GENERATE_EMBEDDING 테스트...")

        query = """
        SELECT
          ml_generate_embedding(
            MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
            STRUCT('Hello World, this is a test sentence for BigQuery AI!' AS content)
          ) AS embedding
        """

        print("   🔍 실행할 쿼리:")
        print(f"   {query.strip()}")

        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            print("   ✅ ML.GENERATE_EMBEDDING 성공!")
            print("   📊 임베딩 생성됨")

            # 임베딩 벡터 정보 출력
            if hasattr(row.embedding, "__len__"):
                print(f"   📏 임베딩 차원: {len(row.embedding)}")
            else:
                print("   📏 임베딩 타입: ", type(row.embedding))

            break

        # 3. 여러 문장에 대한 임베딩 생성 테스트
        print("\n3️⃣ 여러 문장에 대한 임베딩 생성 테스트...")

        test_sentences = [
            "BigQuery AI provides powerful machine learning capabilities.",
            "Text embeddings help understand semantic relationships.",
            "This is a test for the Kaggle hackathon.",
        ]

        for i, sentence in enumerate(test_sentences, 1):
            try:
                query = f"""
                SELECT
                  ml_generate_embedding(
                    MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
                    STRUCT('{sentence}' AS content)
                  ) AS embedding
                """

                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    print(
                        f"   ✅ 문장 {i} 임베딩 생성 성공: {sentence[:50]}..."
                    )
                    break

            except Exception as e:
                print(f"   ❌ 문장 {i} 임베딩 생성 실패: {str(e)[:100]}...")

        print("\n✅ ML.GENERATE_EMBEDDING 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_ml_generate_embedding()
