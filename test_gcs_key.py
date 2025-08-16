#!/usr/bin/env python3
"""
GCS 키 파일을 사용한 BigQuery 연결 테스트
"""

import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account

def test_gcs_key_connection():
    """GCS 키 파일을 사용한 BigQuery 연결 테스트"""
    
    # 1. GCS 키 파일 경로 설정
    key_path = "gcs-key.json"
    
    if not os.path.exists(key_path):
        print(f"❌ GCS 키 파일을 찾을 수 없음: {key_path}")
        return False
    
    try:
        # 2. 서비스 계정 인증 정보 로드
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        
        print("✅ 서비스 계정 인증 정보 로드 성공")
        
        # 3. BigQuery 클라이언트 생성
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )
        
        print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {credentials.project_id})")
        
        # 4. 간단한 쿼리 테스트
        query = "SELECT 1 as test_value"
        query_job = client.query(query)
        results = query_job.result()
        
        for row in results:
            print(f"✅ 쿼리 테스트 성공: {row.test_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 연결 테스트 실패: {str(e)}")
        return False

def test_public_datasets():
    """공개 데이터셋 접근 테스트"""
    
    try:
        key_path = "gcs-key.json"
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        
        client = bigquery.Client(credentials=credentials)
        
        # 공개 데이터셋 테스트
        test_datasets = [
            "bigquery-public-data.hacker_news.stories",
            "bigquery-public-data.wikipedia.pageviews_2024"
        ]
        
        accessible_datasets = []
        
        for dataset in test_datasets:
            try:
                query = f"SELECT * FROM `{dataset}` LIMIT 1"
                result = client.query(query)
                rows = list(result)
                
                if rows:
                    print(f"✅ 접근 가능: {dataset}")
                    accessible_datasets.append(dataset)
                else:
                    print(f"⚠️ 결과 없음: {dataset}")
                    
            except Exception as e:
                print(f"❌ 접근 불가: {dataset} - {str(e)[:100]}...")
                continue
        
        return len(accessible_datasets) > 0
        
    except Exception as e:
        print(f"❌ 공개 데이터셋 테스트 실패: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🔑 GCS 키 파일 BigQuery 연결 테스트")
    print("=" * 50)
    
    # 1. 기본 연결 테스트
    print("\n1️⃣ 기본 연결 테스트")
    basic_success = test_gcs_key_connection()
    
    # 2. 공개 데이터셋 테스트
    print("\n2️⃣ 공개 데이터셋 접근 테스트")
    dataset_success = test_public_datasets()
    
    # 3. 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    print(f"기본 연결: {'✅ 성공' if basic_success else '❌ 실패'}")
    print(f"데이터셋 접근: {'✅ 성공' if dataset_success else '❌ 실패'}")
    
    if basic_success and dataset_success:
        print("\n🎉 GCS 키 파일로 BigQuery 연결 성공!")
        print("💡 해커톤 진행 가능")
    else:
        print("\n🚨 GCS 키 파일로도 해결되지 않음")
        print("💡 추가 문제 해결 필요")

if __name__ == "__main__":
    main() 