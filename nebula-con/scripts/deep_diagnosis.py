#!/usr/bin/env python3
"""
GCP 환경 심층 진단 스크립트
실행 환경의 모든 변수를 한 번에 점검하여 문제 원인 파악
"""

from google.cloud import bigquery
from google.cloud import bigquery_connection_v1
from google.cloud import aiplatform
import os
import json
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def collect_gcp_environment_info():
    """GCP 환경/리소스 정보를 수집합니다."""
    
    print("🔍 GCP 환경/리소스 정보 수집 시작...")
    
    try:
        # 1. BigQuery 클라이언트 정보
        bq_client = bigquery.Client()
        project_id = bq_client.project
        location = bq_client.location or "미설정"
        
        print(f"\n📊 BigQuery 프로젝트 정보:")
        print(f"  - 프로젝트 ID: {project_id}")
        print(f"  - 리전: {location}")
        
        # 2. 서비스 계정 정보
        service_account = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '미설정')
        print(f"\n🔑 서비스 계정 정보:")
        print(f"  - 인증 파일: {service_account}")
        
        # 3. 데이터셋 정보
        datasets = list(bq_client.list_datasets())
        print(f"\n📁 BigQuery 데이터셋 목록:")
        for dataset in datasets:
            print(f"  - {dataset.dataset_id}")
            
            # 데이터셋 내 테이블 및 모델 확인
            try:
                tables = list(bq_client.list_tables(dataset.dataset_id))
                models = list(bq_client.list_models(dataset.dataset_id))
                
                print(f"    테이블: {len(tables)}개")
                for table in tables:
                    print(f"      - {table.table_id}")
                
                print(f"    모델: {len(models)}개")
                for model in models:
                    print(f"      - {model.model_id} (타입: {model.model_type})")
                    
            except Exception as e:
                print(f"    데이터셋 접근 오류: {str(e)}")
        
        # 4. BigQuery 연결 정보
        print(f"\n🔗 BigQuery 연결 정보:")
        try:
            connection_client = bigquery_connection_v1.ConnectionServiceClient()
            parent = f"projects/{project_id}/locations/us-central1"
            connections = list(connection_client.list_connections(parent=parent))
            
            for connection in connections:
                print(f"  - 연결명: {connection.name}")
                print(f"    상태: {getattr(connection, 'state', '알 수 없음')}")
                if hasattr(connection, 'cloud_resource'):
                    print(f"    리소스: {connection.cloud_resource}")
                    
        except Exception as e:
            print(f"  연결 정보 조회 실패: {str(e)}")
        
        # 5. 환경 변수 확인
        print(f"\n🌍 환경 변수:")
        env_vars = [
            'GOOGLE_CLOUD_PROJECT',
            'GOOGLE_APPLICATION_CREDENTIALS',
            'BIGQUERY_DATASET',
            'VERTEX_AI_LOCATION'
        ]
        
        for var in env_vars:
            value = os.environ.get(var, '미설정')
            print(f"  - {var}: {value}")
        
        return {
            'project_id': project_id,
            'location': location,
            'service_account': service_account,
            'datasets': [d.dataset_id for d in datasets]
        }
        
    except Exception as e:
        print(f"❌ GCP 환경 정보 수집 실패: {str(e)}")
        return None


def test_bigquery_ml_functions():
    """BigQuery ML 함수들의 실제 작동 상태를 테스트합니다."""
    
    print(f"\n🧪 BigQuery ML 함수 테스트 시작...")
    
    try:
        client = bigquery.Client()
        
        # 1. ML.GENERATE_EMBEDDING 테스트
        print(f"\n🔍 ML.GENERATE_EMBEDDING 함수 테스트...")
        
        test_queries = [
            # 기본 구문 테스트
            """
            SELECT ML.GENERATE_EMBEDDING(
                'test text',
                'textembedding-gecko@003'
            ) AS embedding
            """,
            
            # 모델 참조 테스트
            """
            SELECT ML.GENERATE_EMBEDDING(
                MODEL `nebula_con_kaggle.text_embedding_remote_model`,
                (SELECT 'test text' AS content)
            ) AS embedding
            """,
            
            # STRUCT 옵션 테스트
            """
            SELECT ML.GENERATE_EMBEDDING(
                MODEL `nebula_con_kaggle.text_embedding_remote_model`,
                (SELECT 'test text' AS content),
                STRUCT(TRUE AS flatten_json_output)
            ) AS embedding
            """
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n  테스트 {i}:")
            print(f"  쿼리: {query.strip()}")
            
            try:
                result = client.query(query)
                rows = list(result.result())
                print(f"  ✅ 성공: {len(rows)}개 결과")
                
            except Exception as e:
                error_msg = str(e)
                print(f"  ❌ 실패: {error_msg}")
                
                # 오류 상세 분석
                if "MODEL" in error_msg:
                    print(f"    분석: 모델 경로 문제")
                elif "ML.GENERATE_EMBEDDING" in error_msg:
                    print(f"    분석: 함수 미지원")
                elif "permission" in error_msg:
                    print(f"    분석: 권한 문제")
                else:
                    print(f"    분석: 기타 오류")
        
        # 2. AI.GENERATE_TEXT 테스트
        print(f"\n🔍 AI.GENERATE_TEXT 함수 테스트...")
        
        ai_query = """
        SELECT AI.GENERATE_TEXT(
            'Hello, how are you?',
            'gemini-pro'
        ) AS answer
        """
        
        try:
            result = client.query(ai_query)
            rows = list(result.result())
            print(f"  ✅ 성공: {len(rows)}개 결과")
            
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ 실패: {error_msg}")
            
            if "AI.GENERATE_TEXT" in error_msg:
                print(f"    분석: AI 함수 미지원")
            else:
                print(f"    분석: 기타 오류")
        
        return True
        
    except Exception as e:
        print(f"❌ BigQuery ML 함수 테스트 실패: {str(e)}")
        return False


def check_vertex_ai_access():
    """Vertex AI 접근 권한을 확인합니다."""
    
    print(f"\n🔍 Vertex AI 접근 권한 확인...")
    
    try:
        # Vertex AI 초기화 시도
        aiplatform.init(
            project=os.environ.get('GOOGLE_CLOUD_PROJECT', 'persona-diary-service'),
            location='us-central1'
        )
        
        print(f"  ✅ Vertex AI 초기화 성공")
        
        # 모델 접근 테스트
        try:
            from google.cloud.aiplatform import TextEmbeddingModel
            
            model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
            print(f"  ✅ textembedding-gecko@003 모델 접근 성공")
            
        except Exception as e:
            print(f"  ❌ textembedding-gecko@003 모델 접근 실패: {str(e)}")
        
        try:
            from google.cloud.aiplatform import TextGenerationModel
            
            model = TextGenerationModel.from_pretrained("gemini-pro")
            print(f"  ✅ gemini-pro 모델 접근 성공")
            
        except Exception as e:
            print(f"  ❌ gemini-pro 모델 접근 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Vertex AI 초기화 실패: {str(e)}")
        return False


def generate_diagnostic_report():
    """진단 보고서를 생성합니다."""
    
    print(f"\n📋 진단 보고서 생성...")
    
    report = {
        'timestamp': str(datetime.now()),
        'gcp_environment': collect_gcp_environment_info(),
        'bigquery_ml_test': test_bigquery_ml_functions(),
        'vertex_ai_access': check_vertex_ai_access()
    }
    
    # 보고서 저장
    with open('gcp_diagnostic_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ 진단 보고서 저장: gcp_diagnostic_report.json")
    
    return report


def main():
    """메인 실행 함수"""
    print("🚨 GCP 환경 심층 진단 시작...")
    
    try:
        report = generate_diagnostic_report()
        
        print(f"\n🎯 진단 완료!")
        print(f"📊 보고서 파일: gcp_diagnostic_report.json")
        
        return 0
        
    except Exception as e:
        print(f"❌ 진단 실패: {str(e)}")
        return 1


if __name__ == "__main__":
    from datetime import datetime
    exit(main()) 