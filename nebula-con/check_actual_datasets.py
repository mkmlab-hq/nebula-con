#!/usr/bin/env python3
"""
실제 BigQuery 프로젝트에 존재하는 데이터셋과 테이블 확인
정확한 데이터셋 ID를 찾기 위한 진단 스크립트
"""

import logging
from google.cloud import bigquery

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_project_structure():
    """프로젝트 구조 전체 확인"""
    try:
        # BigQuery 클라이언트 초기화
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info("🔍 프로젝트 persona-diary-service 구조 확인 중...")
        
        # 1. 모든 데이터셋 목록 조회
        datasets = list(client.list_datasets())
        logger.info(f"✅ 발견된 데이터셋 수: {len(datasets)}")
        
        for dataset in datasets:
            logger.info(f"📁 데이터셋: {dataset.dataset_id}")
            
            # 2. 각 데이터셋의 테이블 목록 조회
            try:
                tables = list(client.list_tables(dataset.dataset_id))
                logger.info(f"   📋 테이블 수: {len(tables)}")
                
                for table in tables:
                    logger.info(f"      🗃️ 테이블: {table.table_id}")
                    
                    # 3. 테이블 스키마 확인
                    try:
                        table_ref = client.dataset(dataset.dataset_id).table(table.table_id)
                        table_obj = client.get_table(table_ref)
                        
                        if table_obj.schema:
                            logger.info(f"         📊 컬럼 수: {len(table_obj.schema)}")
                            for field in table_obj.schema[:3]:  # 처음 3개 컬럼만
                                logger.info(f"            - {field.name}: {field.field_type}")
                            if len(table_obj.schema) > 3:
                                logger.info(f"            ... (총 {len(table_obj.schema)}개 컬럼)")
                        else:
                            logger.info("         📊 스키마 정보 없음")
                            
                    except Exception as e:
                        logger.error(f"         ❌ 테이블 스키마 확인 실패: {e}")
                        
            except Exception as e:
                logger.error(f"   ❌ 테이블 목록 조회 실패: {e}")
        
        # 4. ML 모델 목록 확인
        logger.info("\n🤖 ML 모델 확인 중...")
        try:
            models = list(client.list_models())
            logger.info(f"✅ 발견된 ML 모델 수: {len(models)}")
            
            for model in models:
                logger.info(f"   🧠 모델: {model.model_id}")
                if hasattr(model, 'model_type'):
                    logger.info(f"      타입: {model.model_type}")
                if hasattr(model, 'remote_service_type'):
                    logger.info(f"      서비스: {model.remote_service_type}")
                    
        except Exception as e:
            logger.error(f"❌ ML 모델 조회 실패: {e}")
        
        # 5. 연결 목록 확인
        logger.info("\n🔗 연결 확인 중...")
        try:
            connections = list(client.list_connections())
            logger.info(f"✅ 발견된 연결 수: {len(connections)}")
            
            for conn in connections:
                logger.info(f"   🔌 연결: {conn.connection_id}")
                if hasattr(conn, 'connection_type'):
                    logger.info(f"      타입: {conn.connection_type}")
                    
        except Exception as e:
            logger.error(f"❌ 연결 조회 실패: {e}")
            
    except Exception as e:
        logger.error(f"❌ 프로젝트 구조 확인 실패: {e}")


def check_specific_dataset(dataset_id):
    """특정 데이터셋 상세 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service', location='US')
        
        logger.info(f"🔍 데이터셋 {dataset_id} 상세 확인 중...")
        
        # 데이터셋 존재 여부 확인
        dataset_ref = client.dataset(dataset_id)
        dataset = client.get_dataset(dataset_ref)
        
        logger.info(f"✅ 데이터셋 {dataset_id} 존재 확인")
        logger.info(f"   📍 위치: {dataset.location}")
        logger.info(f"   📅 생성일: {dataset.created}")
        
        # 테이블 목록
        tables = list(client.list_tables(dataset_id))
        logger.info(f"   📋 테이블 수: {len(tables)}")
        
        for table in tables:
            logger.info(f"      🗃️ 테이블: {table.table_id}")
            
    except Exception as e:
        logger.error(f"❌ 데이터셋 {dataset_id} 확인 실패: {e}")


if __name__ == "__main__":
    # 전체 프로젝트 구조 확인
    check_project_structure()
    
    # 특정 데이터셋들 확인 시도
    test_datasets = [
        'nebula_con',
        'nebula_con_kaggle', 
        'kaggle',
        'hacker_news',
        'default'
    ]
    
    logger.info("\n🔍 특정 데이터셋 존재 여부 확인...")
    for dataset_id in test_datasets:
        try:
            check_specific_dataset(dataset_id)
        except Exception as e:
            logger.info(f"   ❌ 데이터셋 {dataset_id} 존재하지 않음")
    
    logger.info("\n✅ 프로젝트 구조 확인 완료!") 