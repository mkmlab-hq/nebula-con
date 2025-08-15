#!/usr/bin/env python3
"""
최종 ML.GENERATE_EMBEDDING 테스트 - FROM 절 사용
"""

from google.api_core.exceptions import BadRequest
from google.cloud import bigquery


def test_ml_generate_embedding_final():
    """최종 ML.GENERATE_EMBEDDING 테스트"""
    print("🔍 최종 ML.GENERATE_EMBEDDING 테스트 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. ML.GENERATE_EMBEDDING 테스트 (FROM 절 사용)
        print("\n2️⃣ ML.GENERATE_EMBEDDING 테스트 (FROM 절 사용)...")

        query = f"""
        SELECT *
        FROM ML.GENERATE_EMBEDDING(
          MODEL `{project_id}.nebula_con_kaggle.text_embedding_remote_model`,
          (SELECT 'Hello World, this is a test sentence for BigQuery AI!' AS content),
          STRUCT(
            'SEMANTIC_SIMILARITY' AS task_type,
            TRUE AS flatten_json_output,
            256 AS output_dimensionality
          )
        )
        """

        print("   🔍 실행할 쿼리:")
        print(f"   {query.strip()}")

        try:
            job = client.query(query)
            print("   ⏳ 임베딩 생성 중... (잠시 대기)")
            results = job.result()

            print("   ✅ 테스트 성공! 임베딩 결과:")
            for row in results:
                # 결과 컬럼 확인
                print(f"   📊 결과 컬럼: {list(row.keys())}")

                # 임베딩 벡터 출력
                if "ml_generate_embedding_result" in row:
                    embedding = row["ml_generate_embedding_result"]
                    print(f"   📏 임베딩 차원: {len(embedding)}")
                    print(f"   🔢 임베딩 샘플: {embedding[:5]}...")
                else:
                    print(f"   📊 전체 결과: {row}")
                break

            return True

        except BadRequest as e:
            print(f"   ❌ BadRequest 오류: {e}")
            return False
        except Exception as e:
            print(f"   ❌ 기타 오류: {e}")
            return False

    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_ml_generate_embedding_final()
