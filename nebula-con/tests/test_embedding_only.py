#!/usr/bin/env python3
"""
임베딩 모델만으로 ML.GENERATE_EMBEDDING 함수 테스트
"""

import os
from google.cloud import bigquery

def test_embedding_function():
    """ML.GENERATE_EMBEDDING 함수 테스트"""
    try:
        # 환경 변수에서 프로젝트 정보 가져오기
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'persona-diary-service')
        dataset_id = os.environ.get('BIGQUERY_DATASET', 'nebula_con_kaggle')
        
        print(f"🧪 ML.GENERATE_EMBEDDING 함수 테스트 시작...")
        print(f"프로젝트: {project_id}, 데이터셋: {dataset_id}")
        
        # BigQuery 클라이언트 초기화
        bq_client = bigquery.Client(project=project_id, location='us-central1')
        
        # ML.GENERATE_EMBEDDING 테스트
        print("🔍 ML.GENERATE_EMBEDDING 함수 테스트...")
        embedding_test_sql = f"""
        SELECT ml_generate_embedding_result
        FROM ML.GENERATE_EMBEDDING(
            MODEL `{project_id}.{dataset_id}.embedding_model`,
            (SELECT 'Hello, this is a test text for embedding generation.' AS content)
        )
        LIMIT 1
        """
        
        try:
            result = bq_client.query(embedding_test_sql)
            rows = list(result.result())
            if rows:
                print("✅ ML.GENERATE_EMBEDDING 함수 테스트 성공!")
                print(f"결과: {rows[0].ml_generate_embedding_result[:100]}...")
                
                # 결과 상세 분석
                embedding_result = rows[0].ml_generate_embedding_result
                if hasattr(embedding_result, 'values'):
                    print(f"임베딩 차원: {len(embedding_result.values)}")
                    print(f"첫 번째 값: {embedding_result.values[0]}")
                else:
                    print(f"임베딩 결과 타입: {type(embedding_result)}")
                    print(f"임베딩 결과: {embedding_result}")
                
                return True
            else:
                print("⚠️ ML.GENERATE_EMBEDDING 테스트 결과가 비어있습니다")
                return False
                
        except Exception as e:
            print(f"❌ ML.GENERATE_EMBEDDING 테스트 실패: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ 테스트 실행 실패: {str(e)}")
        return False


if __name__ == "__main__":
    test_embedding_function() 