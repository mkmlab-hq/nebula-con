#!/usr/bin/env python3
"""
자체 테스트 데이터로 임베딩 생성
"""

from google.cloud import bigquery


def generate_test_embeddings():
    """자체 테스트 데이터로 임베딩 생성"""
    print("🔧 자체 테스트 데이터로 임베딩 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 초기화
        print("\n1️⃣ BigQuery 클라이언트 초기화...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 테스트 문장들로 임베딩 생성
        print("\n2️⃣ 테스트 문장들로 임베딩 생성...")

        test_sentences = [
            "BigQuery AI provides powerful machine learning capabilities.",
            "Text embeddings help understand semantic relationships.",
            "This is a test for the Kaggle hackathon.",
            "Machine learning models can generate high-quality embeddings.",
            "Natural language processing is essential for AI applications.",
            "BigQuery ML enables easy model training and deployment.",
            "Vector search improves information retrieval accuracy.",
            "Semantic similarity helps find related content.",
            "AI-powered text analysis enhances user experience.",
            "Cloud computing scales machine learning workloads.",
        ]

        print(f"   📝 {len(test_sentences)}개 테스트 문장 준비 완료")

        # 3. 임베딩 생성 쿼리
        print("\n3️⃣ 임베딩 생성 쿼리 실행...")

        embedding_query = f"""
        SELECT *
        FROM ML.GENERATE_EMBEDDING(
          MODEL `{project_id}.nebula_con_kaggle.text_embedding_remote_model`,
          (
            SELECT sentence AS content
            FROM UNNEST([
              {", ".join([f"'{sentence}'" for sentence in test_sentences])}
            ]) AS sentence
          ),
          STRUCT(
            'SEMANTIC_SIMILARITY' AS task_type,
            TRUE AS flatten_json_output,
            768 AS output_dimensionality
          )
        )
        """

        print("   🔍 실행할 쿼리:")
        print(f"   {embedding_query.strip()}")

        # 4. 결과를 새 테이블에 저장
        print("\n4️⃣ 결과를 새 테이블에 저장...")

        job_config = bigquery.QueryJobConfig(
            destination=client.dataset("nebula_con_kaggle").table("test_embeddings"),
            write_disposition="WRITE_TRUNCATE",
        )

        job = client.query(embedding_query, job_config=job_config)
        print("   ⏳ 임베딩 생성 및 저장 중... (잠시 대기)")
        job.result()

        print("   ✅ 테스트 데이터 임베딩 생성 및 저장 완료!")
        print("   📍 저장 위치: nebula_con_kaggle.test_embeddings")

        # 5. 결과 확인
        print("\n5️⃣ 결과 확인...")

        table_ref = client.dataset("nebula_con_kaggle").table("test_embeddings")
        table = client.get_table(table_ref)

        print(f"   📊 테이블 행 수: {table.num_rows:,}")
        print("   📋 스키마:")
        for field in table.schema:
            print(f"      - {field.name}: {field.field_type}")

        # 6. 샘플 데이터 확인
        print("\n6️⃣ 샘플 데이터 확인...")

        sample_query = f"""
  SELECT content,
               ARRAY_LENGTH(ml_generate_embedding_result) as embedding_dim,
               ml_generate_embedding_statistics
        FROM `{project_id}.nebula_con_kaggle.test_embeddings`
        LIMIT 3
        """

        sample_results = client.query(sample_query).result()
        print("   🔍 샘플 데이터:")
        for i, row in enumerate(sample_results, 1):
            print(f"      {i}. 텍스트: {row.content[:50]}...")
            print(f"         임베딩 차원: {row.embedding_dim}")
            print(f"         통계: {row.ml_generate_embedding_statistics}")

        print("\n🎉 테스트 임베딩 생성 완료!")
        print("   📋 다음 단계:")
        print("   1. 캐글 실제 데이터셋 경로 확인")
        print("   2. 실제 데이터로 임베딩 생성")
        print("   3. Baseline 모델 제출")

        return True

    except Exception as e:
        print(f"\n❌ 임베딩 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    generate_test_embeddings()
