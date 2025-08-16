#!/usr/bin/env python3
"""
BigQuery 환경 종합 진단 스크립트
404 오류와 ML 기능 실패의 근본 원인 파악
"""

import logging
from google.cloud import bigquery
from google.api_core.exceptions import Forbidden, NotFound, BadRequest

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def diagnose_project_access():
    """프로젝트 접근 권한 진단"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("🔍 프로젝트 접근 권한 진단 시작...")
        
        # 1. 프로젝트 정보 확인
        project = client.get_project()
        logger.info(f"✅ 프로젝트 접근 성공: {project.project_id}")
        logger.info(f"   📍 위치: {project.location}")
        logger.info(f"   📅 생성일: {project.created}")
        
        # 2. 데이터셋 목록 조회 시도
        try:
            datasets = list(client.list_datasets())
            logger.info(f"✅ 데이터셋 목록 조회 성공: {len(datasets)}개 발견")
            
            for dataset in datasets:
                logger.info(f"   📁 {dataset.dataset_id} ({dataset.location})")
                
        except Forbidden as e:
            logger.error(f"❌ 데이터셋 목록 조회 권한 없음: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 데이터셋 목록 조회 실패: {e}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 프로젝트 접근 실패: {e}")
        return False


def diagnose_dataset_issues():
    """데이터셋 관련 문제 진단"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("\n🔍 데이터셋 문제 진단 시작...")
        
        # 1. 존재하지 않는 데이터셋들 확인
        non_existent_datasets = [
            'nebula_con',
            'nebula_con_kaggle',
            'kaggle',
            'hacker_news'
        ]
        
        for dataset_id in non_existent_datasets:
            try:
                dataset_ref = client.dataset(dataset_id)
                dataset = client.get_dataset(dataset_ref)
                logger.info(f"✅ {dataset_id}: 존재함 ({dataset.location})")
            except NotFound:
                logger.error(f"❌ {dataset_id}: 404 Not Found")
            except Exception as e:
                logger.error(f"❌ {dataset_id}: 오류 발생 - {e}")
        
        # 2. 실제 존재하는 데이터셋 상세 확인
        try:
            # us-central1 위치에서 데이터셋 확인
            client_us_central1 = bigquery.Client(
                project='persona-diary-service', location='us-central1'
            )
            
            datasets = list(client_us_central1.list_datasets())
            logger.info(f"\n📍 us-central1 위치 데이터셋:")
            
            for dataset in datasets:
                logger.info(f"   📁 {dataset.dataset_id}")
                
                # 테이블 목록 확인
                try:
                    tables = list(client_us_central1.list_tables(dataset.dataset_id))
                    logger.info(f"      📋 테이블 {len(tables)}개")
                    
                    for table in tables:
                        logger.info(f"         🗃️ {table.table_id}")
                        
                except Exception as e:
                    logger.error(f"      ❌ 테이블 목록 조회 실패: {e}")
                    
        except Exception as e:
            logger.error(f"❌ us-central1 위치 확인 실패: {e}")
            
    except Exception as e:
        logger.error(f"❌ 데이터셋 진단 실패: {e}")


def diagnose_ml_capabilities():
    """BigQuery ML 기능 진단"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("\n🔍 BigQuery ML 기능 진단 시작...")
        
        # 1. ML 모델 목록 확인
        try:
            # 기본 위치에서 모델 확인
            models = list(client.list_models())
            logger.info(f"✅ ML 모델 {len(models)}개 발견")
            
            for model in models:
                logger.info(f"   🧠 {model.model_id}")
                if hasattr(model, 'model_type'):
                    logger.info(f"      타입: {model.model_type}")
                    
        except Exception as e:
            logger.error(f"❌ ML 모델 조회 실패: {e}")
        
        # 2. us-central1 위치에서 ML 모델 확인
        try:
            client_us_central1 = bigquery.Client(
                project='persona-diary-service', location='us-central1'
            )
            
            models = list(client_us_central1.list_models())
            logger.info(f"\n📍 us-central1 위치 ML 모델:")
            
            for model in models:
                logger.info(f"   🧠 {model.model_id}")
                if hasattr(model, 'model_type'):
                    logger.info(f"      타입: {model.model_type}")
                    
        except Exception as e:
            logger.error(f"❌ us-central1 ML 모델 조회 실패: {e}")
            
    except Exception as e:
        logger.error(f"❌ ML 기능 진단 실패: {e}")


def diagnose_connections():
    """BigQuery 연결 진단"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("\n🔍 BigQuery 연결 진단 시작...")
        
        # 1. 연결 목록 확인 시도
        try:
            # 기본 위치에서 연결 확인
            connections = list(client.list_connections())
            logger.info(f"✅ 연결 {len(connections)}개 발견")
            
            for conn in connections:
                logger.info(f"   🔌 {conn.connection_id}")
                if hasattr(conn, 'connection_type'):
                    logger.info(f"      타입: {conn.connection_type}")
                    
        except Exception as e:
            logger.error(f"❌ 연결 목록 조회 실패: {e}")
        
        # 2. us-central1 위치에서 연결 확인
        try:
            client_us_central1 = bigquery.Client(
                project='persona-diary-service', location='us-central1'
            )
            
            connections = list(client_us_central1.list_connections())
            logger.info(f"\n📍 us-central1 위치 연결:")
            
            for conn in connections:
                logger.info(f"   🔌 {conn.connection_id}")
                if hasattr(conn, 'connection_type'):
                    logger.info(f"      타입: {conn.connection_type}")
                    
        except Exception as e:
            logger.error(f"❌ us-central1 연결 조회 실패: {e}")
            
    except Exception as e:
        logger.error(f"❌ 연결 진단 실패: {e}")


def test_ml_functions():
    """ML 함수 실제 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("\n🔍 ML 함수 실제 테스트 시작...")
        
        # 1. ML.GENERATE_EMBEDDING 테스트
        try:
            test_query = """
            SELECT ml_generate_embedding_result
            FROM ML.GENERATE_EMBEDDING(
              MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_model`,
              (SELECT 'test text' AS content)
            )
            """
            
            logger.info("🧪 ML.GENERATE_EMBEDDING 테스트 실행...")
            result = client.query(test_query)
            rows = list(result.result())
            
            if rows:
                logger.info("✅ ML.GENERATE_EMBEDDING 테스트 성공!")
            else:
                logger.warning("⚠️ ML.GENERATE_EMBEDDING 결과 없음")
                
        except NotFound as e:
            logger.error(f"❌ ML.GENERATE_EMBEDDING: 모델을 찾을 수 없음 - {e}")
        except BadRequest as e:
            logger.error(f"❌ ML.GENERATE_EMBEDDING: 구문 오류 - {e}")
        except Exception as e:
            logger.error(f"❌ ML.GENERATE_EMBEDDING: 예상치 못한 오류 - {e}")
            
    except Exception as e:
        logger.error(f"❌ ML 함수 테스트 실패: {e}")


def generate_solution_report():
    """진단 결과 기반 솔루션 리포트 생성"""
    logger.info("\n📋 진단 결과 기반 솔루션 리포트")
    logger.info("=" * 50)
    
    logger.info("\n🚨 즉시 해결해야 할 문제들:")
    logger.info("1. 데이터셋 위치 불일치: US vs us-central1")
    logger.info("2. ML 모델 존재하지 않음")
    logger.info("3. Vertex AI 연결 설정 누락")
    logger.info("4. 권한 및 역할 확인 필요")
    
    logger.info("\n🔧 단계별 해결 방안:")
    logger.info("1단계: BigQuery 콘솔에서 데이터셋 위치 확인")
    logger.info("2단계: Vertex AI 연결 생성")
    logger.info("3단계: 원격 ML 모델 생성")
    logger.info("4단계: ML 함수 테스트")
    
    logger.info("\n⏰ 예상 소요 시간: 2-4시간")
    logger.info("🎯 목표: 해커톤 제출 가능한 완전한 RAG 파이프라인")


if __name__ == "__main__":
    logger.info("🚀 BigQuery 환경 종합 진단 시작")
    
    # 1. 프로젝트 접근 권한 진단
    if diagnose_project_access():
        # 2. 데이터셋 문제 진단
        diagnose_dataset_issues()
        
        # 3. ML 기능 진단
        diagnose_ml_capabilities()
        
        # 4. 연결 진단
        diagnose_connections()
        
        # 5. ML 함수 실제 테스트
        test_ml_functions()
        
        # 6. 솔루션 리포트 생성
        generate_solution_report()
    else:
        logger.error("❌ 프로젝트 접근 실패로 인한 진단 중단")
    
    logger.info("\n✅ BigQuery 환경 진단 완료") 