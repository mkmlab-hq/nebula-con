#!/usr/bin/env python3
"""
여러 문장에 대한 임베딩 생성 테스트
"""

from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


def test_multiple_embeddings():
    """여러 문장에 대한 임베딩 생성 테스트"""
    print("🔍 여러 문장에 대한 임베딩 생성 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 테스트 문장들
        test_sentences = [
            "BigQuery AI provides powerful machine learning capabilities.",
            "Text embeddings help understand semantic relationships.",
            "This is a test for the Kaggle hackathon.",
            "Machine learning models can generate high-quality embeddings.",
            "Natural language processing is essential for AI applications.",
        ]

        print(f"\n2️⃣ {len(test_sentences)}개 문장에 대한 임베딩 생성...")

        for i, sentence in enumerate(test_sentences, 1):
            print(f"\n   🔍 문장 {i}: {sentence}")

            query = f"""
            SELECT 
              content,
              ml_generate_embedding_result,
              ml_generate_embedding_statistics
            FROM ML.GENERATE_EMBEDDING(
              MODEL `{project_id}.nebula_con_kaggle.text_embedding_remote_model`,
              (SELECT '{sentence}' AS content),
              STRUCT(
                'SEMANTIC_SIMILARITY' AS task_type,
                TRUE AS flatten_json_output
              )
            )
            """

            try:
                job = client.query(query)
                results = job.result()

                for row in results:
                    embedding = row["ml_generate_embedding_result"]
                    stats = row["ml_generate_embedding_statistics"]

                    print(f"      ✅ 임베딩 생성 성공!")
                    print(f"         📏 차원: {len(embedding)}")
                    print(f"         🔢 샘플: {embedding[:3]}...")
                    print(f"         📊 통계: 토큰 {stats['token_count']}개")
                    break

            except Exception as e:
                print(f"      ❌ 임베딩 생성 실패: {str(e)[:100]}...")

        print("\n✅ 모든 문장에 대한 임베딩 생성 테스트 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_multiple_embeddings()
