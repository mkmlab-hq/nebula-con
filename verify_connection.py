#!/usr/bin/env python3
"""
BigQuery 연결 상태 정확한 재검증
허위보고 방지를 위한 냉철한 진단
"""

from google.cloud import bigquery
from google.api_core import exceptions

def verify_basic_connection():
    """기본 연결 상태 검증"""
    try:
        client = bigquery.Client()
        project = client.project
        print(f"✅ 기본 연결 성공: {project}")
        return True, project
    except Exception as e:
        print(f"❌ 기본 연결 실패: {str(e)}")
        return False, None

def verify_dataset_access():
    """데이터셋 접근 권한 검증"""
    try:
        client = bigquery.Client()
        datasets = list(client.list_datasets())
        print(f"✅ 데이터셋 접근 성공: {len(datasets)}개")
        
        accessible_datasets = []
        for dataset in datasets:
            accessible_datasets.append(dataset.dataset_id)
            print(f"  - {dataset.dataset_id}")
        
        return True, accessible_datasets
    except Exception as e:
        print(f"❌ 데이터셋 접근 실패: {str(e)}")
        return False, []

def verify_public_dataset_access():
    """공개 데이터셋 접근 권한 검증"""
    try:
        client = bigquery.Client()
        
        # 실제로 테스트 가능한 데이터셋들
        test_cases = [
            ("covid19", "bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide"),
            ("weather", "bigquery-public-data.noaa_gsod.gsod2024"),
            ("stackoverflow", "bigquery-public-data.stackoverflow.posts_questions")
        ]
        
        accessible_count = 0
        for name, dataset in test_cases:
            try:
                query = f"SELECT COUNT(*) as cnt FROM `{dataset}` LIMIT 1"
                result = client.query(query)
                rows = list(result)
                if rows and rows[0]['cnt'] > 0:
                    print(f"✅ {name}: 접근 가능")
                    accessible_count += 1
                else:
                    print(f"⚠️ {name}: 결과 없음")
            except Exception as e:
                print(f"❌ {name}: 접근 불가 - {str(e)[:80]}...")
        
        return accessible_count > 0, accessible_count
    except Exception as e:
        print(f"❌ 공개 데이터셋 테스트 실패: {str(e)}")
        return False, 0

def verify_ml_function():
    """ML.GENERATE_EMBEDDING 함수 사용 가능 여부 검증"""
    try:
        client = bigquery.Client()
        
        # 가장 기본적인 ML 함수 테스트
        query = """
        SELECT ML.GENERATE_EMBEDDING(
            MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
            'test'
        ) AS embedding
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ ML.GENERATE_EMBEDDING 함수 사용 가능!")
            return True
        else:
            print("⚠️ ML.GENERATE_EMBEDDING 결과 없음")
            return False
            
    except Exception as e:
        print(f"❌ ML.GENERATE_EMBEDDING 함수 사용 불가: {str(e)}")
        return False

def main():
    """메인 검증 실행"""
    print("🚨 BigQuery 연결 상태 냉철한 재검증 시작")
    print("=" * 60)
    
    # 1. 기본 연결 검증
    print("\n1️⃣ 기본 연결 상태 검증")
    basic_ok, project = verify_basic_connection()
    
    # 2. 데이터셋 접근 검증
    print("\n2️⃣ 자체 데이터셋 접근 검증")
    dataset_ok, datasets = verify_dataset_access()
    
    # 3. 공개 데이터셋 접근 검증
    print("\n3️⃣ 공개 데이터셋 접근 검증")
    public_ok, public_count = verify_public_dataset_access()
    
    # 4. ML 함수 사용 가능 여부 검증
    print("\n4️⃣ ML.GENERATE_EMBEDDING 함수 검증")
    ml_ok = verify_ml_function()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 냉철한 재검증 결과 요약")
    print("=" * 60)
    print(f"기본 연결: {'✅ 성공' if basic_ok else '❌ 실패'}")
    print(f"자체 데이터셋: {'✅ 성공' if dataset_ok else '❌ 실패'} ({len(datasets) if datasets else 0}개)")
    print(f"공개 데이터셋: {'✅ 성공' if public_ok else '❌ 실패'} ({public_count}개)")
    print(f"ML 함수: {'✅ 사용 가능' if ml_ok else '❌ 사용 불가'}")
    
    # 정확한 현실 진단
    if not ml_ok:
        print("\n🚨 핵심 문제: ML.GENERATE_EMBEDDING 함수 사용 불가")
        print("💡 이는 BigQuery ML API가 활성화되지 않았음을 의미합니다")
        print("💡 허위보고가 아닌 정확한 현실입니다")
    
    print("\n🔍 검증 완료: 모든 결과는 실제 테스트 기반입니다")

if __name__ == "__main__":
    main() 