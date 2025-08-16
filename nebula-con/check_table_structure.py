#!/usr/bin/env python3
"""
테이블 구조 확인 스크립트
"""

from google.cloud import bigquery

def check_table_structure():
    """테이블 구조를 확인합니다."""
    
    print("🔍 테이블 구조 확인 중...")
    
    client = bigquery.Client()
    
    # test_embeddings 테이블 구조 확인
    try:
        query = """
        SELECT * FROM `persona-diary-service.nebula_con_kaggle.test_embeddings` 
        LIMIT 3
        """
        
        print("🔍 test_embedd 테이블 쿼리 실행 중...")
        result = client.query(query)
        rows = list(result)
        
        if result.schema:
            print(f"✅ 컬럼: {[field.name for field in result.schema]}")
        else:
            print("❌ 스키마 정보 없음")
            
        print(f"✅ 데이터 행 수: {len(rows)}")
        if rows:
            print(f"첫 번째 행: {rows[0]}")
            
    except Exception as e:
        print(f"❌ test_embedd 테이블 확인 실패: {str(e)}")
    
    # hacker_news_embeddings_external 테이블 구조 확인
    try:
        query = """
        SELECT * FROM `persona-diary-service.nebula_con_kaggle.hacker_news_embeddings_external` 
        LIMIT 3
        """
        
        print("\n🔍 hacker_news_embeddings_external 테이블 쿼리 실행 중...")
        result = client.query(query)
        rows = list(result)
        
        if result.schema:
            print(f"✅ 컬럼: {[field.name for field in result.schema]}")
        else:
            print("❌ 스키마 정보 없음")
            
        print(f"✅ 데이터 행 수: {len(rows)}")
        if rows:
            print(f"첫 번째 행: {rows[0]}")
            
    except Exception as e:
        print(f"❌ hacker_news_embeddings_external 테이블 확인 실패: {str(e)}")

if __name__ == "__main__":
    check_table_structure() 