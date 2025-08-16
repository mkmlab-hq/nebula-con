#!/usr/bin/env python3
"""
기존 BigQuery 연결 상태 확인 스크립트
"""

import os
from google.cloud import bigquery
from google.cloud import bigquery_connection_v1

def check_existing_connections():
    """기존 연결 상태 확인"""
    try:
        # 환경 변수에서 프로젝트 정보 가져오기
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'persona-diary-service')
        location = 'us-central1'
        
        print(f"🔍 프로젝트 {project_id}의 연결 상태 확인 중...")
        
        # BigQuery 클라이언트 초기화
        bq_client = bigquery.Client(project=project_id, location=location)
        
        # 연결 클라이언트 초기화
        connection_client = bigquery_connection_v1.ConnectionServiceClient()
        
        # 연결 목록 조회
        parent = f"projects/{project_id}/locations/{location}"
        connections = connection_client.list_connections(parent=parent)
        
        print(f"✅ 연결 목록 조회 완료:")
        connection_count = 0
        
        for connection in connections:
            connection_count += 1
            print(f"  {connection_count}. 연결명: {connection.name}")
            print(f"     상태: {connection.state}")
            if hasattr(connection, 'cloud_resource'):
                print(f"     리소스: {connection.cloud_resource}")
            print()
        
        if connection_count == 0:
            print("⚠️ 활성화된 연결이 없습니다")
            print("💡 BigQuery ML API를 사용하려면 연결이 필요합니다")
        
        # 모델 목록도 확인
        print(f"🔍 데이터셋 {project_id}.nebula_con_kaggle의 모델 확인 중...")
        try:
            models = list(bq_client.list_models(f'{project_id}.nebula_con_kaggle'))
            print(f"✅ 모델 수: {len(models)}개")
            
            for model in models:
                print(f"  - 모델: {model.model_id}")
                print(f"    타입: {model.model_type}")
                print(f"    생성일: {model.created}")
                print()
                
        except Exception as e:
            print(f"❌ 모델 목록 조회 실패: {str(e)}")
        
        return connection_count > 0
        
    except Exception as e:
        print(f"❌ 연결 상태 확인 실패: {str(e)}")
        return False

if __name__ == "__main__":
    check_existing_connections() 