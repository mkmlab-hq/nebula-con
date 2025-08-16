#!/usr/bin/env python3
"""
BigQuery 위치 문제 해결 테스트
공식 문서 기반 정확한 접근 방법 시도
"""

from google.cloud import bigquery
from google.api_core import exceptions

def test_location_specific_queries():
    """위치별 쿼리 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 위치별 쿼리 테스트 시작...")
        
        # 테스트 1: US 위치에서 공개 데이터셋 접근
        print("\n1️⃣ US 위치에서 공개 데이터셋 테스트")
        query1 = """
        SELECT COUNT(*) as cnt
        FROM `bigquery-public-data.samples.shakespeare`
        LIMIT 1
        """
        
        try:
            result1 = client.query(query1)
            rows1 = list(result1)
            if rows1:
                print("✅ US 위치 공개 데이터셋 접근 성공!")
                print(f"  결과: {rows1[0]['cnt']}")
                return True
            else:
                print("⚠️ US 위치 결과 없음")
        except Exception as e:
            print(f"❌ US 위치 접근 실패: {str(e)[:100]}...")
        
        # 테스트 2: EU 위치에서 공개 데이터셋 접근
        print("\n2️⃣ EU 위치에서 공개 데이터셋 테스트")
        query2 = """
        SELECT COUNT(*) as cnt
        FROM `bigquery-public-data.samples.shakespeare`
        LIMIT 1
        """
        
        try:
            # EU 위치로 설정
            job_config = bigquery.QueryJobConfig()
            job_config.location = 'EU'
            
            result2 = client.query(query2, job_config=job_config)
            rows2 = list(result2)
            if rows2:
                print("✅ EU 위치 공개 데이터셋 접근 성공!")
                print(f"  결과: {rows2[0]['cnt']}")
                return True
            else:
                print("⚠️ EU 위치 결과 없음")
        except Exception as e:
            print(f"❌ EU 위치 접근 실패: {str(e)[:100]}...")
        
        # 테스트 3: asia-northeast3 위치에서 공개 데이터셋 접근
        print("\n3️⃣ asia-northeast3 위치에서 공개 데이터셋 테스트")
        query3 = """
        SELECT COUNT(*) as cnt
        FROM `bigquery-public-data.samples.shakespeare`
        LIMIT 1
        """
        
        try:
            # asia-northeast3 위치로 설정
            job_config = bigquery.QueryJobConfig()
            job_config.location = 'asia-northeast3'
            
            result3 = client.query(query3, job_config=job_config)
            rows3 = list(result3)
            if rows3:
                print("✅ asia-northeast3 위치 공개 데이터셋 접근 성공!")
                print(f"  결과: {rows3[0]['cnt']}")
                return True
            else:
                print("⚠️ asia-northeast3 위치 결과 없음")
        except Exception as e:
            print(f"❌ asia-northeast3 위치 접근 실패: {str(e)[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ 위치별 쿼리 테스트 오류: {str(e)}")
        return False

def test_ml_function_with_location():
    """위치를 지정하여 ML 함수 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 위치 지정 ML.GENERATE_EMBEDDING 테스트...")
        
        # 다양한 위치에서 ML 함수 테스트
        locations = ['US', 'EU', 'asia-northeast3']
        
        for location in locations:
            try:
                print(f"\n📍 {location} 위치에서 ML 함수 테스트...")
                
                query = """
                SELECT ML.GENERATE_EMBEDDING(
                    MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
                    'Hello, this is a test'
                ) AS embedding
                """
                
                job_config = bigquery.QueryJobConfig()
                job_config.location = location
                
                result = client.query(query, job_config=job_config)
                rows = list(result)
                
                if rows:
                    print(f"🎉 {location} 위치에서 ML 함수 성공!")
                    print(f"  임베딩 차원: {len(rows[0]['embedding'])}")
                    return True
                else:
                    print(f"⚠️ {location} 위치에서 결과 없음")
                    
            except Exception as e:
                print(f"❌ {location} 위치에서 ML 함수 실패: {str(e)[:100]}...")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ 위치 지정 ML 함수 테스트 오류: {str(e)}")
        return False

def test_public_dataset_list():
    """사용 가능한 공개 데이터셋 목록 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 사용 가능한 공개 데이터셋 확인...")
        
        # 공식 문서에 나온 샘플 데이터셋들 테스트
        sample_datasets = [
            "bigquery-public-data.samples.shakespeare",
            "bigquery-public-data.samples.github_nested",
            "bigquery-public-data.samples.github_timeline",
            "bigquery-public-data.samples.natality",
            "bigquery-public-data.samples.trigrams",
            "bigquery-public-data.samples.wikipedia"
        ]
        
        accessible_count = 0
        for dataset in sample_datasets:
            try:
                query = f"SELECT COUNT(*) as cnt FROM `{dataset}` LIMIT 1"
                result = client.query(query)
                rows = list(result)
                
                if rows and rows[0]['cnt'] > 0:
                    print(f"✅ {dataset}: 접근 가능")
                    accessible_count += 1
                else:
                    print(f"⚠️ {dataset}: 결과 없음")
                    
            except Exception as e:
                print(f"❌ {dataset}: 접근 불가 - {str(e)[:80]}...")
        
        return accessible_count > 0, accessible_count
        
    except Exception as e:
        print(f"❌ 공개 데이터셋 목록 테스트 오류: {str(e)}")
        return False, 0

def main():
    """메인 테스트 실행"""
    print("🚀 BigQuery 위치 문제 해결 테스트 시작")
    print("=" * 70)
    
    # 1. 위치별 쿼리 테스트
    location_success = test_location_specific_queries()
    
    # 2. 위치 지정 ML 함수 테스트
    ml_location_success = test_ml_function_with_location()
    
    # 3. 공개 데이터셋 목록 확인
    public_success, public_count = test_public_dataset_list()
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("📊 위치 문제 해결 테스트 결과 요약")
    print("=" * 70)
    print(f"위치별 쿼리: {'✅ 성공' if location_success else '❌ 실패'}")
    print(f"위치 지정 ML 함수: {'✅ 성공' if ml_location_success else '❌ 실패'}")
    print(f"공개 데이터셋: {'✅ 성공' if public_success else '❌ 실패'} ({public_count}개)")
    
    if location_success or ml_location_success:
        print("\n🎉 위치 문제 해결 성공!")
        print("💡 공식 문서 기반 접근 방법이 작동합니다!")
    else:
        print("\n🚨 위치 문제로도 해결되지 않음")
        print("💡 근본적인 BigQuery ML API 권한 문제입니다")
    
    print("\n🔍 모든 테스트는 공식 문서 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 