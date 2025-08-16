#!/usr/bin/env python3
"""
Shakespeare 데이터셋으로 임베딩 생성
"""

from google.cloud import bigquery


def generate_shakespeare_embeddings():
    """Shakespeare 데이터셋으로 임베딩 생성"""
    print("🔧 Shakespeare 데이터셋으로 임베딩 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 초기화
        print("\n1️⃣ BigQuery 클라이언트 초기화...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. Shakespeare 데이터셋 정보 확인
        print("\n2️⃣ Shakespeare 데이터셋 정보 확인...")

        shakespeare_table = "bigquery-public-data.samples.shakespeare"

        # 데이터 샘플 확인
        sample_query = f"""
        SELECT word, corpus, word_count
        FROM `{shakespeare_table}`
        WHERE LENGTH(word) > 3
        ORDER BY word_count DESC
        LIMIT 10
        """

        sample_results = client.query(sample_query).result()
        print("   📊 Shakespeare 데이터 샘플:")
        for i, row in enumerate(sample_results, 1):
            print(
                f"      {i}. 단어: '{row.word}' (빈도: {row.word_count}, 코퍼스: {row.corpus})"
            )

        # 3. 임베딩 생성 (상위 빈도 단어들)
        print("\n3️⃣ 상위 빈도 단어들로 임베딩 생성...")

        embedding_query = f"""
        SELECT *
        FROM ML.GENERATE_EMBEDDING(
          MODEL `{project_id}.nebula_con_kaggle.text_embedding_remote_model`,
          (
            SELECT
              CONCAT(word, ' (', corpus, ')') AS content
            FROM `{shakespeare_table}`
            WHERE LENGTH(word) > 3
            AND word_count > 100
            ORDER BY word_count DESC
            LIMIT 1000  -- 상위 1000개 단어
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
            destination=client.dataset("nebula_con_kaggle").table(
                "shakespeare_embeddings"
            ),
            write_disposition="WRITE_TRUNCATE",
        )

        job = client.query(embedding_query, job_config=job_config)
        print("   ⏳ 임베딩 생성 및 저장 중... (잠시 대기)")
        job.result()

        print("   ✅ Shakespeare 데이터 임베딩 생성 및 저장 완료!")
        print("   📍 저장 위치: nebula_con_kaggle.shakespeare_embeddings")

        # 5. 결과 확인
        print("\n5️⃣ 결과 확인...")

        table_ref = client.dataset("nebula_con_kaggle").table("shakespeare_embeddings")
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
        FROM `{project_id}.nebula_con_kaggle.shakespeare_embeddings`
        LIMIT 5
        """

        sample_results = client.query(sample_query).result()
        print("   🔍 샘플 데이터:")
        for i, row in enumerate(sample_results, 1):
            print(f"      {i}. 텍스트: {row.content}")
            print(f"         임베딩 차원: {row.embedding_dim}")
            print(f"         통계: {row.ml_generate_embedding_statistics}")

        print("\n🎉 Shakespeare 임베딩 생성 완료!")
        print("   📋 다음 단계:")
        print("   1. 임베딩 기반 유사도 검색 테스트")
        print("   2. Baseline 모델 제출 준비")
        print("   3. 캐글 해커톤 점수 획득")

        return True

    except Exception as e:
        print(f"\n❌ 임베딩 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    generate_shakespeare_embeddings()
