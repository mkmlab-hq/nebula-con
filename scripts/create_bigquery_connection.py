#!/usr/bin/env python3
"""
BigQuery Connection 생성 스크립트
"""

from google.cloud import bigquery, bigquery_connection_v1
from google.cloud.bigquery_connection_v1 import CloudResourceProperties, Connection


def create_bigquery_connection():
    """BigQuery Connection 생성"""
    print("🔧 BigQuery Connection 생성 시작...")

    try:
        # 1. BigQuery 클라이언트 생성
        print("\n1️⃣ BigQuery 클라이언트 생성...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. BigQuery Connection 클라이언트 생성
        print("\n2️⃣ BigQuery Connection 클라이언트 생성...")
        connection_client = bigquery_connection_v1.ConnectionServiceClient()
        parent = f"projects/{project_id}/locations/us-central1"
        print("   📍 위치: us-central1")

        # 3. Connection 생성
        print("\n3️⃣ Connection 생성 중...")

        connection = Connection(
            cloud_resource=CloudResourceProperties(service_account_id="")
        )

        connection_client.create_connection(
            parent=parent,
            connection_id="my_vertex_ai_connection",
            connection=connection,
        )

        print("   ✅ Connection 생성 요청 완료!")
        print("   ⏳ 생성 완료까지 잠시 기다려주세요...")

        # 4. 생성된 Connection 정보 확인
        print("\n4️⃣ 생성된 Connection 정보 확인...")

        # 잠시 대기 후 확인
        import time

        time.sleep(10)

        connection_path = f"{parent}/connections/my_vertex_ai_connection"
        connection_info = connection_client.get_connection(name=connection_path)

        print("   ✅ Connection 생성 완료!")
        print(f"   🔗 Connection 이름: {connection_info.name}")

        if connection_info.cloud_resource.service_account_id:
            print(
                f"   👤 서비스 계정: "
                f"{connection_info.cloud_resource.service_account_id}"
            )
            print("\n   📋 다음 단계:")
            print("   1. 위 서비스 계정에 'Vertex AI 사용자' 역할 부여")
            print("   2. Remote Model 생성")
            print("   3. ML.GENERATE_EMBEDDING 테스트")

        return True

    except Exception as e:
        print(f"\n❌ Connection 생성 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return False


if __name__ == "__main__":
    create_bigquery_connection()
