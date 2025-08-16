#!/usr/bin/env python3
"""
BigQuery ML API 상태 확인 스크립트
"""

from google.cloud import bigquery
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_bigquery_ml_api():
    """BigQuery ML API 상태를 확인합니다."""
    
    print("🔍 BigQuery ML API 상태 확인 중...")
    
    try:
        client = bigquery.Client()
        print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {client.project})")
        
        # 1. 간단한 ML 함수 테스트
        print("\n🔍 ML.GENERATE_EMBEDDING 함수 테스트...")
        
        test_query = """
        SELECT 
            ML.GENERATE_EMBEDDING(
                MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
                (SELECT 'test text' AS content),
                STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_DOCUMENT' AS task_type)
            ) AS embedding
        LIMIT 1
        """
        
        print(f"테스트 쿼리: {test_query}")
        
        try:
            result = client.query(test_query)
            rows = list(result.result())
            print("✅ ML.GENERATE_EMBEDDING 함수 정상 작동!")
            print(f"결과: {len(rows)}개 행")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ML.GENERATE_EMBEDDING 함수 오류: {error_msg}")
            
            # 오류 분석
            if "ML.GENERATE_EMBEDDING" in error_msg:
                print("🔍 분석: ML.GENERATE_EMBEDDING 함수가 지원되지 않음")
            elif "MODEL" in error_msg:
                print("🔍 분석: MODEL 키워드 구문 오류")
            elif "API" in error_msg:
                print("🔍 분석: BigQuery ML API 활성화 필요")
            else:
                print("🔍 분석: 기타 BigQuery ML 관련 오류")
        
        # 2. AI.GENERATE_TEXT 함수 테스트
        print("\n🔍 AI.GENERATE_TEXT 함수 테스트...")
        
        ai_test_query = """
        SELECT 
            AI.GENERATE_TEXT(
                'Hello, how are you?',
                'gemini-pro'
            ) AS answer
        LIMIT 1
        """
        
        print(f"AI 테스트 쿼리: {ai_test_query}")
        
        try:
            result = client.query(ai_test_query)
            rows = list(result.result())
            print("✅ AI.GENERATE_TEXT 함수 정상 작동!")
            print(f"결과: {len(rows)}개 행")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ AI.GENERATE_TEXT 함수 오류: {error_msg}")
            
            # 오류 분석
            if "AI.GENERATE_TEXT" in error_msg:
                print("🔍 분석: AI.GENERATE_TEXT 함수가 지원되지 않음")
            elif "API" in error_msg:
                print("🔍 분석: BigQuery AI API 활성화 필요")
            else:
                print("🔍 분석: 기타 BigQuery AI 관련 오류")
        
        # 3. API 활성화 상태 확인
        print("\n🔍 API 활성화 상태 확인...")
        
        try:
            # BigQuery ML 모델 목록 확인
            models = list(client.list_models('persona-diary-service.nebula_con_kaggle'))
            print(f"✅ 데이터셋 내 모델 수: {len(models)}개")
            
            for model in models:
                print(f"  - 모델: {model.model_id}")
                print(f"    타입: {model.model_type}")
                print(f"    생성일: {model.created}")
                
        except Exception as e:
            print(f"❌ 모델 목록 확인 실패: {str(e)}")
        
        # 4. 권한 상태 확인
        print("\n🔍 권한 상태 확인...")
        
        try:
            # 현재 사용자 정보 확인
            query = "SELECT SESSION_USER() as current_user"
            result = client.query(query)
            user_info = list(result.result())[0]
            print(f"✅ 현재 사용자: {user_info.current_user}")
            
        except Exception as e:
            print(f"❌ 사용자 정보 확인 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ BigQuery ML API 상태 확인 실패: {str(e)}")
        return False


def main():
    """메인 실행 함수"""
    print("🚀 BigQuery ML API 상태 확인 시작...")
    
    success = check_bigquery_ml_api()
    
    if success:
        print("\n✅ BigQuery ML API 상태 확인 완료!")
    else:
        print("\n❌ BigQuery ML API 상태 확인 실패!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 