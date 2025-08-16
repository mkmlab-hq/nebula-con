#!/usr/bin/env python3
"""
BigQuery Remote Model 수정 스크립트
MODEL_TYPE_UNSPECIFIED 문제를 해결하여 정상 작동하는 모델로 재생성
"""

from google.cloud import bigquery
from google.cloud import bigquery_connection_v1
import logging
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def delete_existing_model():
    """기존의 문제가 있는 모델을 삭제합니다."""
    
    print("🗑️ 기존 모델 삭제 시작...")
    
    try:
        client = bigquery.Client()
        
        # 기존 모델 삭제
        model_id = "text_embedding_remote_model"
        dataset_id = "nebula_con_kaggle"
        project_id = client.project
        
        model_path = f"{project_id}.{dataset_id}.{model_id}"
        
        print(f"🔍 모델 경로: {model_path}")
        
        # 모델 존재 여부 확인
        try:
            model = client.get_model(model_path)
            print(f"✅ 모델 발견: {model.model_id}")
            print(f"   타입: {model.model_type}")
            print(f"   생성일: {model.created}")
            
            # 모델 삭제
            client.delete_model(model_path)
            print(f"🗑️ 모델 삭제 완료: {model_id}")
            
        except Exception as e:
            print(f"❌ 모델 삭제 실패: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 모델 삭제 중 오류 발생: {str(e)}")
        return False


def recreate_remote_model():
    """올바른 설정으로 Remote Model을 재생성합니다."""
    
    print("\n🔧 Remote Model 재생성 시작...")
    
    try:
        client = bigquery.Client()
        
        # 모델 생성 쿼리
        create_model_query = """
        CREATE OR REPLACE MODEL `nebula_con_kaggle.text_embedding_remote_model`
        OPTIONS(
            model_type='REMOTE',
            connection='projects/persona-diary-service/locations/us-central1/connections/my_vertex_ai_connection',
            remote_service_type='CLOUD_AI_SERVICE_V1',
            endpoint='projects/907685055657/locations/us-central1/publishers/google/models/textembedding-gecko@003'
        )
        """
        
        print("🔍 모델 생성 쿼리 실행 중...")
        print(f"쿼리: {create_model_query}")
        
        # 모델 생성
        job = client.query(create_model_query)
        job.result()  # 완료 대기
        
        print("✅ Remote Model 재생성 완료!")
        
        # 모델 상태 확인
        model_id = "text_embedding_remote_model"
        dataset_id = "nebula_con_kaggle"
        project_id = client.project
        
        model_path = f"{project_id}.{dataset_id}.{model_id}"
        
        try:
            model = client.get_model(model_path)
            print(f"\n🔍 재생성된 모델 정보:")
            print(f"  - 모델 ID: {model.model_id}")
            print(f"  - 타입: {model.model_type}")
            print(f"  - 생성일: {model.created}")
            print(f"  - 수정일: {model.modified}")
            
            if hasattr(model, 'labels'):
                print(f"  - 라벨: {model.labels}")
                
        except Exception as e:
            print(f"❌ 모델 정보 확인 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Remote Model 재생성 실패: {str(e)}")
        return False


def test_model_functionality():
    """재생성된 모델의 기능을 테스트합니다."""
    
    print("\n🧪 모델 기능 테스트 시작...")
    
    try:
        client = bigquery.Client()
        
        # ML.GENERATE_EMBEDDING 함수 테스트
        test_query = """
        SELECT 
            ML.GENERATE_EMBEDDING(
                MODEL `nebula_con_kaggle.text_embedding_remote_model`,
                (SELECT 'test text for embedding' AS content),
                STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_DOCUMENT' AS task_type)
            ) AS embedding
        LIMIT 1
        """
        
        print("🔍 ML.GENERATE_EMBEDDING 함수 테스트...")
        print(f"테스트 쿼리: {test_query}")
        
        try:
            result = client.query(test_query)
            rows = list(result.result())
            print("✅ ML.GENERATE_EMBEDDING 함수 정상 작동!")
            print(f"결과: {len(rows)}개 행")
            
            # 결과 상세 확인
            if rows:
                embedding_result = rows[0].embedding
                print(f"임베딩 결과 타입: {type(embedding_result)}")
                if hasattr(embedding_result, 'values'):
                    print(f"임베딩 차원: {len(embedding_result.values)}")
                else:
                    print(f"임베딩 내용: {embedding_result}")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ML.GENERATE_EMBEDDING 함수 테스트 실패: {error_msg}")
            
            # 오류 분석
            if "MODEL" in error_msg:
                print("🔍 분석: 모델 경로 또는 설정 문제")
            elif "connection" in error_msg:
                print("🔍 분석: Vertex AI 연결 문제")
            elif "endpoint" in error_msg:
                print("🔍 분석: 모델 엔드포인트 문제")
            else:
                print("🔍 분석: 기타 BigQuery ML 관련 오류")
            
            return False
        
    except Exception as e:
        print(f"❌ 모델 기능 테스트 실패: {str(e)}")
        return False


def main():
    """메인 실행 함수"""
    print("🚨 BigQuery Remote Model 수정 시작...")
    
    try:
        # 1단계: 기존 모델 삭제
        if not delete_existing_model():
            print("❌ 기존 모델 삭제 실패")
            return 1
        
        # 2단계: Remote Model 재생성
        if not recreate_remote_model():
            print("❌ Remote Model 재생성 실패")
            return 1
        
        # 3단계: 모델 기능 테스트
        if not test_model_functionality():
            print("❌ 모델 기능 테스트 실패")
            return 1
        
        print("\n🎉 BigQuery Remote Model 수정 완료!")
        print("✅ 이제 ML.GENERATE_EMBEDDING 함수를 사용할 수 있습니다!")
        
        return 0
        
    except Exception as e:
        print(f"❌ 메인 실행 오류: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 