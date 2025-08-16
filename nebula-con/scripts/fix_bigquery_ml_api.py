#!/usr/bin/env python3
"""
BigQuery ML API 문제 해결 스크립트
연결 및 원격 모델 생성으로 ML.GENERATE_EMBEDDING과 ML.GENERATE_TEXT 활성화
"""

import os
import logging
from google.cloud import bigquery
from google.cloud import bigquery_connection_v1

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BigQueryMLAPIFixer:
    """BigQuery ML API 문제 해결 클래스"""
    
    def __init__(self, project_id: str, dataset_id: str, location: str = 'us-central1'):
        """초기화"""
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.location = location
        
        # BigQuery 클라이언트 초기화
        self.bq_client = bigquery.Client(project=project_id, location=location)
        
        # BigQuery 연결 클라이언트 초기화
        self.connection_client = bigquery_connection_v1.ConnectionServiceClient()
        
        logger.info("✅ BigQuery ML API 수정기 초기화 완료")
        logger.info(f"프로젝트: {project_id}, 데이터셋: {dataset_id}, "
                   f"지역: {location}")
    
    def create_cloud_resource_connection(
        self, connection_id: str = 'my-connection'
    ) -> bool:
        """클라우드 리소스 연결 생성"""
        try:
            logger.info(f"🔗 클라우드 리소스 연결 생성 중: {connection_id}")
            
            # 연결 생성 SQL
            connection_sql = f"""
            CREATE OR REPLACE CONNECTION 
            `{self.project_id}.{self.location}.{connection_id}`
            OPTIONS (TYPE = 'CLOUD_RESOURCE')
            """
            
            # SQL 실행
            result = self.bq_client.query(connection_sql)
            result.result()  # 완료 대기
            
            logger.info(f"✅ 클라우드 리소스 연결 생성 완료: {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 연결 생성 실패: {str(e)}")
            return False
    
    def get_connection_service_account(self, connection_id: str = 'my-connection') -> str:
        """연결의 서비스 계정 ID 조회"""
        try:
            logger.info(f"🔍 연결 서비스 계정 조회 중: {connection_id}")
            
            # 서비스 계정 조회 SQL
            query_sql = f"""
            SELECT service_account_id 
            FROM `{self.location}`.INFORMATION_SCHEMA.CONNECTIONS 
            WHERE connection_id = '{connection_id}'
            """
            
            result = self.bq_client.query(query_sql)
            rows = list(result.result())
            
            if rows:
                service_account = rows[0].service_account_id
                logger.info(f"✅ 서비스 계정 조회 완료: {service_account}")
                return service_account
            else:
                logger.warning("⚠️ 서비스 계정을 찾을 수 없습니다")
                return ""
                
        except Exception as e:
            logger.error(f"❌ 서비스 계정 조회 실패: {str(e)}")
            return ""
    
    def create_embedding_model(self, connection_id: str = 'my-connection') -> bool:
        """임베딩 모델 생성"""
        try:
            logger.info("🤖 임베딩 모델 생성 중...")
            
            # 임베딩 모델 생성 SQL
            model_sql = f"""
            CREATE OR REPLACE MODEL 
            `{self.project_id}.{self.dataset_id}.embedding_model`
            REMOTE WITH CONNECTION 
            `{self.project_id}.{self.location}.{connection_id}`
            OPTIONS (ENDPOINT = 'text-embedding-004')
            """
            
            # SQL 실행
            result = self.bq_client.query(model_sql)
            result.result()  # 완료 대기
            
            logger.info("✅ 임베딩 모델 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 임베딩 모델 생성 실패: {str(e)}")
            return False
    
    def create_text_model(self, connection_id: str = 'my-connection') -> bool:
        """텍스트 생성 모델 생성"""
        try:
            logger.info("🤖 텍스트 생성 모델 생성 중...")
            
            # 텍스트 모델 생성 SQL
            model_sql = f"""
            CREATE OR REPLACE MODEL `{self.project_id}.{self.dataset_id}.text_model`
            REMOTE WITH CONNECTION `{self.project_id}.{self.location}.{connection_id}`
            OPTIONS (ENDPOINT = 'gemini-1.5-flash-001')
            """
            
            # SQL 실행
            result = self.bq_client.query(model_sql)
            result.result()  # 완료 대기
            
            logger.info("✅ 텍스트 생성 모델 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 텍스트 생성 모델 생성 실패: {str(e)}")
            return False
    
    def test_ml_generate_embedding(self) -> bool:
        """ML.GENERATE_EMBEDDING 함수 테스트"""
        try:
            logger.info("🧪 ML.GENERATE_EMBEDDING 함수 테스트 중...")
            
            # 테스트 쿼리
            test_query = f"""
            SELECT ml_generate_embedding_result
            FROM ML.GENERATE_EMBEDDING(
                MODEL `{self.project_id}.{self.dataset_id}.embedding_model`,
                (SELECT 'Hello, this is a test text for embedding generation.' AS content)
            )
            LIMIT 1
            """
            
            # 쿼리 실행
            result = self.bq_client.query(test_query)
            rows = list(result.result())
            
            if rows:
                logger.info("✅ ML.GENERATE_EMBEDDING 함수 테스트 성공!")
                logger.info(f"결과: {rows[0].ml_generate_embedding_result[:100]}...")
                return True
            else:
                logger.warning("⚠️ 테스트 결과가 비어있습니다")
                return False
                
        except Exception as e:
            logger.error(f"❌ ML.GENERATE_EMBEDDING 테스트 실패: {str(e)}")
            return False
    
    def test_ml_generate_text(self) -> bool:
        """ML.GENERATE_TEXT 함수 테스트"""
        try:
            logger.info("🧪 ML.GENERATE_TEXT 함수 테스트 중...")
            
            # 테스트 쿼리
            test_query = f"""
            SELECT ml_generate_text_result
            FROM ML.GENERATE_TEXT(
                MODEL `{self.project_id}.{self.dataset_id}.text_model`,
                'What is artificial intelligence?'
            )
            LIMIT 1
            """
            
            # 쿼리 실행
            result = self.bq_client.query(test_query)
            rows = list(result.result())
            
            if rows:
                logger.info("✅ ML.GENERATE_TEXT 함수 테스트 성공!")
                logger.info(f"결과: {rows[0].ml_generate_text_result[:100]}...")
                return True
            else:
                logger.warning("⚠️ 테스트 결과가 비어있습니다")
                return False
                
        except Exception as e:
            logger.error(f"❌ ML.GENERATE_TEXT 테스트 실패: {str(e)}")
            return False
    
    def run_full_fix(self) -> bool:
        """전체 수정 과정 실행"""
        try:
            logger.info("🚀 BigQuery ML API 전체 수정 과정 시작...")
            
            # 1. 클라우드 리소스 연결 생성
            if not self.create_cloud_resource_connection():
                logger.error("❌ 연결 생성 실패로 수정 중단")
                return False
            
            # 2. 서비스 계정 확인
            service_account = self.get_connection_service_account()
            if service_account:
                logger.info(f"📋 서비스 계정: {service_account}")
                logger.info("💡 이 계정에 'Vertex AI User' 및 'BigQuery Connection User' 역할이 부여되어 있는지 확인하세요")
            
            # 3. 임베딩 모델 생성
            if not self.create_embedding_model():
                logger.error("❌ 임베딩 모델 생성 실패")
                return False
            
            # 4. 텍스트 모델 생성
            if not self.create_text_model():
                logger.error("❌ 텍스트 모델 생성 실패")
                return False
            
            # 5. 함수 테스트
            logger.info("🧪 생성된 모델들로 함수 테스트 시작...")
            
            embedding_test = self.test_ml_generate_embedding()
            text_test = self.test_ml_generate_text()
            
            if embedding_test and text_test:
                logger.info("🎉 모든 테스트 통과! BigQuery ML API 문제 해결 완료!")
                return True
            else:
                logger.warning("⚠️ 일부 테스트 실패. 권한 설정을 확인하세요")
                return False
                
        except Exception as e:
            logger.error(f"❌ 전체 수정 과정 실패: {str(e)}")
            return False


def main():
    """메인 실행 함수"""
    try:
        # 환경 변수에서 프로젝트 정보 가져오기
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'persona-diary-service')
        dataset_id = os.environ.get('BIGQUERY_DATASET', 'nebula_con_kaggle')
        
        logger.info("🚀 BigQuery ML API 문제 해결 시작...")
        logger.info(f"프로젝트: {project_id}")
        logger.info(f"데이터셋: {dataset_id}")
        
        # 수정기 초기화 및 실행
        fixer = BigQueryMLAPIFixer(project_id, dataset_id)
        success = fixer.run_full_fix()
        
        if success:
            print("\n🎉 BigQuery ML API 문제 해결 완료!")
            print("✅ 이제 ML.GENERATE_EMBEDDING과 ML.GENERATE_TEXT 함수를 사용할 수 있습니다!")
            print("🚀 RAG 파이프라인을 정상적으로 실행할 수 있습니다!")
            print("💡 해커톤 제출 준비가 완료되었습니다!")
        else:
            print("\n❌ BigQuery ML API 문제 해결 실패")
            print("🔍 로그를 확인하여 구체적인 오류를 파악하세요")
            return 1
            
        return 0
        
    except Exception as e:
        print(f"❌ 메인 실행 오류: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 