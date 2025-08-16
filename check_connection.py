#!/usr/bin/env python3
"""
Vertex AI Connection 존재 여부 확인
text_embedding_remote_model 생성 전 필수 Connection 상태 점검
"""

from google.cloud import bigquery
from google.api_core import exceptions

def check_vertex_ai_connection():
    """Vertex AI Connection 존재 여부 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 Vertex AI Connection 존재 여부 확인...")
        
        # 방법 1: EXTERNAL_CONNECTIONS에서 확인
        query1 = """
        SELECT connection_id, connection_type, properties
        FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
        WHERE connection_id = 'my_vertex_ai_connection'
        """
        
        try:
            result1 = client.query(query1)
            rows1 = list(result1)
            
            if rows1:
                print("✅ my_vertex_ai_connection 발견!")
                for row in rows1:
                    print(f"  - Connection ID: {row['connection_id']}")
                    print(f"  - Connection Type: {row['connection_type']}")
                    print(f"  - Properties: {row['properties']}")
                return True
            else:
                print("⚠️ my_vertex_ai_connection이 EXTERNAL_CONNECTIONS에 없습니다")
                
        except Exception as e:
            print(f"❌ EXTERNAL_CONNECTIONS 확인 실패: {str(e)[:100]}...")
        
        # 방법 2: 데이터셋 내 모든 Connection 확인
        print("\n🔍 데이터셋 내 모든 Connection 확인...")
        try:
            query2 = """
            SELECT connection_id, connection_type
            FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
            """
            
            result2 = client.query(query2)
            rows2 = list(result2)
            
            if rows2:
                print("데이터셋 'nebula_con_kaggle' 내 Connection:")
                for row in rows2:
                    print(f"  - {row['connection_id']}: {row['connection_type']}")
            else:
                print("⚠️ 데이터셋에 Connection이 없습니다")
                
        except Exception as e:
            print(f"❌ Connection 목록 확인 실패: {str(e)[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ Connection 확인 오류: {str(e)}")
        return False

def create_vertex_ai_connection():
    """Vertex AI Connection 생성 시도"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 Vertex AI Connection 생성 시도...")
        
        # Connection 생성 SQL
        create_connection_sql = """
        CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
        OPTIONS (
          connection_type = 'CLOUD_RESOURCE',
          resource_uri = '//aiplatform.googleapis.com/projects/persona-diary-service/locations/us-central1'
        )
        """
        
        try:
            result = client.query(create_connection_sql)
            result.result()  # 작업 완료 대기
            print("✅ Vertex AI Connection 생성 성공!")
            return True
            
        except Exception as e:
            print(f"❌ Connection 생성 실패: {str(e)[:100]}...")
            return False
        
    except Exception as e:
        print(f"❌ Connection 생성 시도 오류: {str(e)}")
        return False

def main():
    """메인 확인 실행"""
    print("🚀 Vertex AI Connection 상태 확인 및 생성 시작")
    print("=" * 80)
    
    # 1. Connection 존재 여부 확인
    connection_exists = check_vertex_ai_connection()
    
    # 2. Connection이 없으면 생성 시도
    if not connection_exists:
        print("\n🚨 my_vertex_ai_connection이 존재하지 않습니다!")
        print("💡 Connection 생성을 시도합니다...")
        
        connection_created = create_vertex_ai_connection()
        
        if connection_created:
            print("\n🎉 Connection 생성 완료! 이제 원격 모델을 생성할 수 있습니다!")
        else:
            print("\n❌ Connection 생성 실패!")
            print("💡 해결방법: BigQuery 콘솔에서 수동으로 Connection을 생성해야 합니다")
    else:
        print("\n✅ Connection이 이미 존재합니다! 원격 모델 생성을 진행할 수 있습니다!")
    
    print("\n🔍 모든 확인은 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 