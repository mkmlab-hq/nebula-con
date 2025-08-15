#!/usr/bin/env python3
"""
캐글 데이터셋에 임베딩 생성 및 저장
"""

from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


def generate_kaggle_embeddings():
    """캐글 데이터셋에 임베딩 생성 및 저장"""
    print("🔧 캐글 데이터셋에 임베딩 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 초기화
        print("\n1️⃣ BigQuery 클라이언트 초기화...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 캐글 데이터셋 쿼리 및 임베딩 생성
        print("\n2️⃣ 캐글 데이터셋 쿼리 및 임베딩 생성...")

        # 캐글 제공 BigQuery 데이터셋 예시
        # 실제 캐글 대회 데이터셋 경로로 변경 필요
        kaggle_table = (
            "bigquery-public-data.stackoverflow.posts.posts_questions"
        )
        text_column = "title"  # 실제 텍스트 컬럼명으로 변경

        print(f"   📊 소스 테이블: {kaggle_table}")
        print(f"   📝 텍스트 컬럼: {text_column}")

        # 임베딩 생성 쿼리
        query = f"""
        SELECT *
        FROM ML.GENERATE_EMBEDDING(
          MODEL `{project_id}.nebula_con_kaggle.text_embedding_remote_model`,
          (
            SELECT {text_column} AS content
            FROM `{kaggle_table}`
            WHERE {text_column} IS NOT NULL 
            AND LENGTH({text_column}) > 10
            LIMIT 1000  -- 테스트용 제한
          ),
          STRUCT(
            'SEMANTIC_SIMILARITY' AS task_type,
            TRUE AS flatten_json_output,
            768 AS output_dimensionality
          )
        )
        """

        print("   🔍 실행할 쿼리:")
        print(f"   {query.strip()}")

        # 3. 결과를 새 테이블에 저장
        print("\n3️⃣ 결과를 새 테이블에 저장...")

        job_config = bigquery.QueryJobConfig(
            destination=client.dataset("nebula_con_kaggle").table(
                "kaggle_embeddings"
            ),
            write_disposition="WRITE_TRUNCATE",  # 기존 테이블 덮어쓰기
        )

        try:
            job = client.query(query, job_config=job_config)
            print("   ⏳ 임베딩 생성 및 저장 중... (잠시 대기)")
            job.result()

            print("   ✅ 캐글 데이터 임베딩 생성 및 저장 완료!")
            print("   📍 저장 위치: nebula_con_kaggle.kaggle_embeddings")

            # 4. 결과 확인
            print("\n4️⃣ 결과 확인...")

            # 저장된 테이블 정보 확인
            table_ref = client.dataset("nebula_con_kaggle").table(
                "kaggle_embeddings"
            )
            table = client.get_table(table_ref)

            print(f"   📊 테이블 행 수: {table.num_rows:,}")
            print(f"   📋 스키마:")
            for field in table.schema:
                print(f"      - {field.name}: {field.field_type}")

            # 샘플 데이터 확인
            sample_query = f"""
            SELECT content, 
                   ARRAY_LENGTH(ml_generate_embedding_result) as embedding_dim,
                   ml_generate_embedding_statistics
            FROM `{project_id}.nebula_con_kaggle.kaggle_embeddings`
            LIMIT 3
            """

            sample_results = client.query(sample_query).result()
            print(f"\n   🔍 샘플 데이터:")
            for i, row in enumerate(sample_results, 1):
                print(f"      {i}. 텍스트: {row.content[:50]}...")
                print(f"         임베딩 차원: {row.embedding_dim}")
                print(f"         통계: {row.ml_generate_embedding_statistics}")

            return True

        except BadRequest as e:
            print(f"   ❌ BadRequest 오류: {e}")
            return False
        except Exception as e:
            print(f"   ❌ 기타 오류: {e}")
            return False

    except Exception as e:
        print(f"\n❌ 임베딩 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    generate_kaggle_embeddings()
