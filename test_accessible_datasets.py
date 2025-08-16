#!/usr/bin/env python3
"""
BigQuery에서 실제로 접근 가능한 데이터셋 찾기
"""

from google.cloud import bigquery
from google.api_core import exceptions

def test_accessible_datasets():
    """접근 가능한 데이터셋 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 접근 가능한 데이터셋 찾는 중...")
        
        # 테스트할 공개 데이터셋들
        test_datasets = [
            "bigquery-public-data.hacker_news.stories",
            "bigquery-public-data.hacker_news.comments", 
            "bigquery-public-data.wikipedia.pageviews_2024",
            "bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide",
            "bigquery-public-data.noaa_gsod.gsod2024",
            "bigquery-public-data.stackoverflow.posts_questions",
            "bigquery-public-data.reddit_comments.2015_05"
        ]
        
        accessible_datasets = []
        
        for dataset in test_datasets:
            try:
                print(f"테스트 중: {dataset}")
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
        
        return accessible_datasets
        
    except Exception as e:
        print(f"❌ 테스트 오류: {str(e)}")
        return []

def test_own_project_access():
    """자체 프로젝트 접근 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 자체 프로젝트 데이터셋 확인 중...")
        
        # 데이터셋 목록 확인
        datasets = list(client.list_datasets())
        print(f"접근 가능한 데이터셋 수: {len(datasets)}")
        
        if datasets:
            print("접근 가능한 데이터셋:")
            for dataset in datasets:
                print(f"  - {dataset.dataset_id}")
                
                # 테이블 목록 확인
                try:
                    tables = list(client.list_tables(dataset))
                    print(f"    테이블 수: {len(tables)}")
                    for table in tables[:3]:  # 처음 3개만 표시
                        print(f"      - {table.table_id}")
                except Exception as e:
                    print(f"    테이블 목록 확인 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 자체 프로젝트 테스트 오류: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 BigQuery 접근 가능한 데이터셋 테스트 시작")
    print("=" * 60)
    
    # 공개 데이터셋 접근 테스트
    accessible_datasets = test_accessible_datasets()
    
    # 자체 프로젝트 접근 테스트
    own_project_success = test_own_project_access()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 데이터셋 접근 테스트 결과 요약")
    print("=" * 60)
    print(f"접근 가능한 공개 데이터셋: {len(accessible_datasets)}개")
    print(f"자체 프로젝트 접근: {'✅ 성공' if own_project_success else '❌ 실패'}")
    
    if accessible_datasets:
        print("\n✅ 접근 가능한 공개 데이터셋:")
        for dataset in accessible_datasets:
            print(f"  - {dataset}")
        
        print("\n💡 다음 단계: 접근 가능한 데이터셋으로 임베딩 테스트")
    else:
        print("\n🚨 공개 데이터셋 접근 불가")
        print("💡 해결방법: 자체 데이터로 임베딩 테스트 진행")

if __name__ == "__main__":
    main() 