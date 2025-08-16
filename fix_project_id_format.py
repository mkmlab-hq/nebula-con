#!/usr/bin/env python3
"""
올바른 프로젝트 ID 형식으로 Connection 확인
BigQuery 문법 규칙에 맞게 백틱 사용
"""

from google.cloud import bigquery
from google.api_core import exceptions

def check_connection_correct_format():
    """올바른 형식으로 Connection 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 올바른 형식으로 Vertex AI Connection 확인...")
        
        # 올바른 형식: 백틱으로 프로젝트 ID 감싸기
        query = """
        SELECT connection_id, connection_type, properties
        FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
        """
        
        try:
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("✅ Connection 발견!")
                for row in rows:
                    print(f"  - {row['connection_id']}: {row['connection_type']}")
                return True
            else:
                print("⚠️ 데이터셋에 Connection이 없습니다")
                return False
                
        except Exception as e:
            print(f"❌ Connection 확인 실패: {str(e)[:100]}...")
            return False
        
    except Exception as e:
        print(f"❌ Connection 확인 오류: {str(e)}")
        return False

def check_dataset_structure():
    """데이터셋 구조 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 데이터셋 구조 확인...")
        
        # 데이터셋 정보 확인
        dataset_ref = client.dataset('nebula_con_kaggle', project='persona-diary-service')
        dataset = client.get_dataset(dataset_ref)
        
        print(f"데이터셋: {dataset.dataset_id}")
        print(f"프로젝트: {dataset.project}")
        print(f"위치: {dataset.location}")
        
        # 테이블 목록
        tables = list(client.list_tables(dataset_ref))
        print(f"\n테이블 수: {len(tables)}")
        for table in tables:
            print(f"  - {table.table_id} ({table.table_type})")
        
        return True
        
    except Exception as e:
        print(f"❌ 데이터셋 구조 확인 오류: {str(e)}")
        return False

def test_simple_query():
    """간단한 쿼리로 기본 연결 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 간단한 쿼리로 기본 연결 테스트...")
        
        # 가장 기본적인 쿼리
        query = """
        SELECT 1 as test
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ 기본 쿼리 성공!")
            return True
        else:
            print("⚠️ 기본 쿼리 결과 없음")
            return False
            
    except Exception as e:
        print(f"❌ 기본 쿼리 테스트 오류: {str(e)}")
        return False

def main():
    """메인 확인 실행"""
    print("🚀 올바른 프로젝트 ID 형식으로 Connection 확인 시작")
    print("=" * 80)
    
    # 1. 기본 연결 테스트
    basic_ok = test_simple_query()
    
    # 2. 데이터셋 구조 확인
    dataset_ok = check_dataset_structure()
    
    # 3. 올바른 형식으로 Connection 확인
    connection_ok = check_connection_correct_format()
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 프로젝트 ID 형식 수정 후 확인 결과 요약")
    print("=" * 80)
    print(f"기본 연결: {'✅ 성공' if basic_ok else '❌ 실패'}")
    print(f"데이터셋 구조: {'✅ 확인됨' if dataset_ok else '❌ 확인 실패'}")
    print(f"Connection 확인: {'✅ 성공' if connection_ok else '❌ 실패'}")
    
    if connection_ok:
        print("\n🎉 Connection 확인 성공! 원격 모델 생성을 진행할 수 있습니다!")
    else:
        print("\n🚨 Connection이 존재하지 않습니다!")
        print("💡 해결방법: BigQuery 콘솔에서 수동으로 Connection을 생성해야 합니다")
        print("💡 또는 공개 ML 모델을 직접 사용하는 방법을 고려해야 합니다")
    
    print("\n🔍 모든 확인은 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 