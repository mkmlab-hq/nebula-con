#!/usr/bin/env python3
"""
환경 변수 및 설정 확인
"""

import os

def check_environment():
    """환경 변수 및 설정을 확인합니다."""
    
    print("🔍 환경 변수 확인:")
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '설정되지 않음')}")
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    
    # GCS 키 파일 존재 여부 확인
    gcs_key = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if gcs_key and os.path.exists(gcs_key):
        print(f"✅ GCS 키 파일 존재: {gcs_key}")
    else:
        print("❌ GCS 키 파일이 존재하지 않거나 경로가 잘못됨")

if __name__ == "__main__":
    check_environment() 