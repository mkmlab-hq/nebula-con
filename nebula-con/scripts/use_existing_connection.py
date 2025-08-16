#!/usr/bin/env python3
"""
기존 연결을 사용하여 BigQuery ML 모델 생성
"""

import os
from google.cloud import bigquery

def create_models_with_existing_connection():
    """기존 연결을 사용하여 모델 생성"""
    try:
        # 환경 변수에서 프로젝트 정보 가져오기
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'persona-diary-service')
        dataset_id = os.environ.get('BIGQUERY_DATASET', 'nebula_con_kaggle')
        location = 'us-central1'
        
        print(f"🔍 프로젝트 {project_id}에서 기존 연결을 사용하여 모델 생성 중...")
        
        # BigQuery 클라이언트 초기화
        bq_client = bigquery.Client(project=project_id, location=location)
        
        # 기존 연결명
        connection_name = f"{project_id}.{location}.my_vertex_ai_connection"
        
        print(f"✅ 기존 연결 사용: {connection_name}")
        
        # 1. 임베딩 모델 생성
        print("🤖 임베딩 모델 생성 중...")
        embedding_model_sql = f"""
        CREATE OR REPLACE MODEL `{project_id}.{dataset_id}.embedding_model`
        REMOTE WITH CONNECTION `{connection_name}`
        OPTIONS (ENDPOINT = 'text-embedding-004')
        """
        
        try:
            result = bq_client.query(embedding_model_sql)
            result.result()  # 완료 대기
            print("✅ 임베딩 모델 생성 완료")
        except Exception as e:
            print(f"❌ 임베딩 모델 생성 실패: {str(e)}")
            return False
        
        # 2. 텍스트 생성 모델 생성
        print("🤖 텍스트 생성 모델 생성 중...")
        text_model_sql = f"""
        CREATE OR REPLACE MODEL `{project_id}.{dataset_id}.text_model`
        REMOTE WITH CONNECTION `{connection_name}`
        OPTIONS (ENDPOINT = 'gemini-pro')
        """
        
        try:
            result = bq_client.query(text_model_sql)
            result.result()  # 완료 대기
            print("✅ 텍스트 생성 모델 생성 완료")
        except Exception as e:
            print(f"❌ 텍스트 생성 모델 생성 실패: {str(e)}")
            return False
        
        # 3. 모델 테스트
        print("🧪 생성된 모델들로 함수 테스트 시작...")
        
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
            else:
                print("⚠️ ML.GENERATE_EMBEDDING 테스트 결과가 비어있습니다")
        except Exception as e:
            print(f"❌ ML.GENERATE_EMBEDDING 테스트 실패: {str(e)}")
        
        # ML.GENERATE_TEXT 테스트
        print("🔍 ML.GENERATE_TEXT 함수 테스트...")
        text_test_sql = f"""
        SELECT ml_generate_text_result
        FROM ML.GENERATE_TEXT(
            MODEL `{project_id}.{dataset_id}.text_model`,
            'What is artificial intelligence?'
        )
        LIMIT 1
        """
        
        try:
            result = bq_client.query(text_test_sql)
            rows = list(result.result())
            if rows:
                print("✅ ML.GENERATE_TEXT 함수 테스트 성공!")
                print(f"결과: {rows[0].ml_generate_text_result[:100]}...")
            else:
                print("⚠️ ML.GENERATE_TEXT 테스트 결과가 비어있습니다")
        except Exception as e:
            print(f"❌ ML.GENERATE_TEXT 테스트 실패: {str(e)}")
        
        print("\n🎉 BigQuery ML 모델 생성 및 테스트 완료!")
        print("✅ 이제 ML.GENERATE_EMBEDDING과 ML.GENERATE_TEXT 함수를 사용할 수 있습니다!")
        
        return True
        
    except Exception as e:
        print(f"❌ 모델 생성 실패: {str(e)}")
        return False


if __name__ == "__main__":
    create_models_with_existing_connection() 