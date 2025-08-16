#!/usr/bin/env python3
"""
BigQuery Connection API를 사용하여 Vertex AI Connection 생성
올바른 방법으로 Connection을 생성합니다.
"""

from google.cloud import bigquery
from google.api_core import exceptions
import json

def create_vertex_ai_connection():
    """BigQuery Connection API를 사용하여 Vertex AI Connection 생성"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 BigQuery Connection API를 사용하여 Vertex AI Connection 생성...")
        
        # BigQuery Connection API를 사용한 Connection 생성
        # 이 방법은 프로그래밍 방식으로 Connection을 생성할 수 있습니다
        
        # 방법 1: BigQuery Connection API 직접 호출
        print("방법 1: BigQuery Connection API 직접 호출...")
        
        # Connection 생성 SQL (BigQuery Connection API 사용)
        create_connection_sql = """
        CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
        OPTIONS (
          connection_type = 'CLOUD_RESOURCE',
          resource_uri = '//aiplatform.googleapis.com/projects/persona-diary-service/locations/us-central1'
        )
        """
        
        try:
            print("Connection 생성 SQL 실행 중...")
            result = client.query(create_connection_sql)
            result.result()  # 작업 완료 대기
            print("✅ Vertex AI Connection 생성 성공!")
            return True
            
        except Exception as e:
            print(f"❌ Connection 생성 실패: {str(e)[:100]}...")
            
            # 방법 2: 다른 Connection 타입 시도
            print("\n방법 2: 다른 Connection 타입 시도...")
            
            create_connection_sql2 = """
            CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
            OPTIONS (
              connection_type = 'CLOUD_RESOURCE'
            )
            """
            
            try:
                result2 = client.query(create_connection_sql2)
                result2.result()
                print("✅ Vertex AI Connection 생성 성공 (간소화된 옵션)!")
                return True
                
            except Exception as e2:
                print(f"❌ 방법 2도 실패: {str(e2)[:100]}...")
                return False
        
    except Exception as e:
        print(f"❌ Connection 생성 시도 오류: {str(e)}")
        return False

def check_existing_connections():
    """기존 Connection 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 기존 Connection 확인...")
        
        # BigQuery Connection API를 통해 Connection 목록 확인
        query = """
        SELECT connection_id, connection_type, properties
        FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
        """
        
        try:
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("✅ 기존 Connection 발견:")
                for row in rows:
                    print(f"  - {row['connection_id']}: {row['connection_type']}")
                return True
            else:
                print("⚠️ 데이터셋에 Connection이 없습니다")
                return False
                
        except Exception as e:
            print(f"❌ Connection 목록 확인 실패: {str(e)[:100]}...")
            return False
        
    except Exception as e:
        print(f"❌ 기존 Connection 확인 오류: {str(e)}")
        return False

def test_ml_embedding_without_connection():
    """Connection 없이 ML.GENERATE_EMBEDDING 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 Connection 없이 ML.GENERATE_EMBEDDING 테스트...")
        
        # 공개 모델을 직접 사용해보기
        query = """
        SELECT ML.GENERATE_EMBEDDING(
          MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
          'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        try:
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("🎉 Connection 없이도 ML.GENERATE_EMBEDDING 성공!")
                print(f"임베딩 차원: {len(rows[0]['embedding'])}")
                return True
            else:
                print("⚠️ 쿼리 결과 없음")
                return False
                
        except Exception as e:
            print(f"❌ ML.GENERATE_EMBEDDING 테스트 실패: {str(e)[:100]}...")
            return False
        
    except Exception as e:
        print(f"❌ ML.GENERATE_EMBEDDING 테스트 오류: {str(e)}")
        return False

def main():
    """메인 실행"""
    print("🚀 BigQuery Connection API를 사용한 Vertex AI Connection 생성 시작")
    print("=" * 80)
    
    # 1. 기존 Connection 확인
    existing_connections = check_existing_connections()
    
    # 2. Connection이 없으면 생성 시도
    if not existing_connections:
        print("\n🚨 my_vertex_ai_connection이 존재하지 않습니다!")
        print("💡 BigQuery Connection API를 사용하여 Connection 생성을 시도합니다...")
        
        connection_created = create_vertex_ai_connection()
        
        if connection_created:
            print("\n🎉 Connection 생성 완료! 이제 원격 모델을 생성할 수 있습니다!")
        else:
            print("\n❌ Connection 생성 실패!")
            print("💡 해결방법: 다른 방법을 시도해야 합니다")
    else:
        print("\n✅ Connection이 이미 존재합니다! 원격 모델 생성을 진행할 수 있습니다!")
    
    # 3. Connection 없이도 ML.GENERATE_EMBEDDING 사용 가능한지 테스트
    print("\n🔍 Connection 없이도 ML.GENERATE_EMBEDDING 사용 가능한지 테스트...")
    ml_ok = test_ml_embedding_without_connection()
    
    if ml_ok:
        print("\n🎉 Connection 없이도 ML.GENERATE_EMBEDDING 사용 가능!")
        print("💡 Kaggle 대회 준비 완료! 해커뉴스 데이터로 임베딩 생성 시작!")
    else:
        print("\n🚨 Connection 없이는 ML.GENERATE_EMBEDDING 사용 불가")
        print("💡 Connection 생성이 반드시 필요합니다")
    
    print("\n🔍 모든 확인은 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 