#!/usr/bin/env python3
"""
GCP API 상태 종합 점검 스크립트
BigQuery ML API 문제 진단 및 해결 방안 제시
"""

from google.cloud import bigquery
from google.cloud import bigquery_connection_v1
import logging
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_gcp_api_status():
    """GCP API 상태를 종합적으로 점검합니다."""
    
    print("🚨 GCP API 상태 종합 점검 시작...")
    
    try:
        client = bigquery.Client()
        print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {client.project})")
        
        # 1. BigQuery ML API 기본 상태 확인
        print("\n🔍 1단계: BigQuery ML API 기본 상태 확인...")
        
        try:
            # 간단한 ML 함수 테스트 (최소한의 구문)
            basic_test_query = """
            SELECT 
                ML.GENERATE_EMBEDDING(
                    MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
                    (SELECT 'test' AS content),
                    STRUCT(TRUE AS flatten_json_output)
                ) AS embedding
            LIMIT 1
            """
            
            print("🔍 기본 ML.GENERATE_EMBEDDING 테스트...")
            result = client.query(basic_test_query)
            rows = list(result.result())
            print("✅ ML.GENERATE_EMBEDDING 함수 정상 작동!")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ML.GENERATE_EMBEDDING 함수 오류: {error_msg}")
            
            # 오류 상세 분석
            if "MODEL" in error_msg and "identifier" in error_msg:
                print("🔍 분석: MODEL 경로 구문 파싱 실패")
                print("🔍 원인: BigQuery ML API가 MODEL 키워드를 인식하지 못함")
                print("🔍 해결방안: API 활성화 상태 확인 필요")
            elif "ML.GENERATE_EMBEDDING" in error_msg:
                print("🔍 분석: ML.GENERATE_EMBEDDING 함수 미지원")
                print("🔍 원인: BigQuery ML API 미활성화")
                print("🔍 해결방안: GCP 콘솔에서 BigQuery ML API 활성화")
            else:
                print("🔍 분석: 기타 BigQuery ML 관련 오류")
        
        # 2. AI.GENERATE_TEXT 함수 테스트
        print("\n🔍 2단계: AI.GENERATE_TEXT 함수 테스트...")
        
        try:
            ai_test_query = """
            SELECT 
                AI.GENERATE_TEXT(
                    'Hello, how are you?',
                    'gemini-pro'
                ) AS answer
            LIMIT 1
            """
            
            result = client.query(ai_test_query)
            rows = list(result.result())
            print("✅ AI.GENERATE_TEXT 함수 정상 작동!")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ AI.GENERATE_TEXT 함수 오류: {error_msg}")
            
            if "Table-valued function is not expected here" in error_msg:
                print("🔍 분석: AI.GENERATE_TEXT 함수 미지원")
                print("🔍 원인: BigQuery AI API 미활성화 또는 제한")
                print("🔍 해결방안: Vertex AI 직접 호출 방식으로 전환")
        
        # 3. BigQuery ML 모델 상태 확인
        print("\n🔍 3단계: BigQuery ML 모델 상태 확인...")
        
        try:
            models = list(client.list_models('persona-diary-service.nebula_con_kaggle'))
            print(f"✅ 데이터셋 내 모델 수: {len(models)}개")
            
            for model in models:
                print(f"  - 모델: {model.model_id}")
                print(f"    타입: {model.model_type}")
                print(f"    생성일: {model.created}")
                print(f"    수정일: {model.modified}")
                
                # 모델 상세 정보 확인
                if hasattr(model, 'labels'):
                    print(f"    라벨: {model.labels}")
                
        except Exception as e:
            print(f"❌ 모델 목록 확인 실패: {str(e)}")
        
        # 4. BigQuery 연결 상태 확인
        print("\n🔍 4단계: BigQuery 연결 상태 확인...")
        
        try:
            # BigQuery 연결 클라이언트 생성
            connection_client = bigquery_connection_v1.ConnectionServiceClient()
            
            # 연결 목록 조회
            parent = f"projects/{client.project}/locations/us-central1"
            connections = connection_client.list_connections(parent=parent)
            
            print("✅ BigQuery 연결 상태:")
            for connection in connections:
                print(f"  - 연결: {connection.name}")
                print(f"    상태: {connection.state}")
                if hasattr(connection, 'cloud_resource'):
                    print(f"    리소스: {connection.cloud_resource}")
                    
        except Exception as e:
            print(f"❌ 연결 상태 확인 실패: {str(e)}")
        
        # 5. 권한 및 인증 상태 확인
        print("\n🔍 5단계: 권한 및 인증 상태 확인...")
        
        try:
            # 현재 사용자 정보 확인
            query = "SELECT SESSION_USER() as current_user, CURRENT_PROJECT() as current_project"
            result = client.query(query)
            user_info = list(result.result())[0]
            print(f"✅ 현재 사용자: {user_info.current_user}")
            print(f"✅ 현재 프로젝트: {user_info.current_project}")
            
        except Exception as e:
            print(f"❌ 사용자 정보 확인 실패: {str(e)}")
        
        # 6. API 할당량 및 제한 확인
        print("\n🔍 6단계: API 할당량 및 제한 확인...")
        
        try:
            # 간단한 쿼리로 할당량 테스트
            quota_test_query = "SELECT 1 as test LIMIT 1"
            result = client.query(quota_test_query)
            rows = list(result.result())
            print("✅ 기본 쿼리 할당량: 정상")
            
        except Exception as e:
            print(f"❌ 할당량 테스트 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ GCP API 상태 점검 실패: {str(e)}")
        return False


def suggest_solutions():
    """문제 해결 방안을 제시합니다."""
    
    print("\n🚨 문제 해결 방안 제시...")
    
    print("\n1️⃣ BigQuery ML API 활성화 확인:")
    print("   - GCP 콘솔 → API 및 서비스 → 라이브러리")
    print("   - 'BigQuery ML API' 검색 및 활성화")
    print("   - 'BigQuery API' 활성화 상태 확인")
    
    print("\n2️⃣ Vertex AI 직접 호출 방식 (권장):")
    print("   - BigQuery ML 함수 대신 Vertex AI Python SDK 사용")
    print("   - textembedding-gecko 모델 직접 호출")
    print("   - gemini-pro 모델 직접 호출")
    
    print("\n3️⃣ 하이브리드 접근법:")
    print("   - BigQuery: 데이터 저장 및 기본 쿼리")
    print("   - Vertex AI: 임베딩 생성 및 AI 답변")
    print("   - Python: 두 서비스 연결 및 조정")
    
    print("\n4️⃣ 즉시 실행 가능한 대안:")
    print("   - 기존 임베딩 테이블 활용")
    print("   - 키워드 기반 검색으로 임시 구현")
    print("   - Vertex AI 직접 호출로 RAG 파이프라인 재구축")


def main():
    """메인 실행 함수"""
    print("🚨 GCP API 상태 종합 점검 시작...")
    
    success = check_gcp_api_status()
    
    if success:
        print("\n✅ GCP API 상태 점검 완료!")
        suggest_solutions()
    else:
        print("\n❌ GCP API 상태 점검 실패!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 