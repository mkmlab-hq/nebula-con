#!/usr/bin/env python3
"""
공개 ML 모델을 직접 사용하여 ML.GENERATE_EMBEDDING 테스트
Connection 없이도 사용 가능한 방법 시도
"""

from google.cloud import bigquery
from google.api_core import exceptions

def test_public_ml_model_direct():
    """공개 ML 모델을 직접 사용하여 ML.GENERATE_EMBEDDING 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 공개 ML 모델을 직접 사용하여 ML.GENERATE_EMBEDDING 테스트...")
        
        # 방법 1: 공개 모델 직접 사용
        query1 = """
        SELECT ML.GENERATE_EMBEDDING(
          MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
          'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        try:
            print("쿼리 1 실행 중...")
            result1 = client.query(query1)
            rows1 = list(result1)
            
            if rows1:
                print("🎉 공개 ML 모델 직접 사용 성공!")
                print(f"임베딩 차원: {len(rows1[0]['embedding'])}")
                print(f"임베딩 샘플: {rows1[0]['embedding'][:5]}...")
                return True
            else:
                print("⚠️ 쿼리 1 결과 없음")
                
        except Exception as e:
            print(f"❌ 쿼리 1 실패: {str(e)[:100]}...")
        
        # 방법 2: 다른 공개 모델 시도
        query2 = """
        SELECT ML.GENERATE_EMBEDDING(
          MODEL `bigquery-public-data.ml_models.textembedding_gecko@001`,
          'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        try:
            print("쿼리 2 실행 중...")
            result2 = client.query(query2)
            rows2 = list(result2)
            
            if rows2:
                print("🎉 공개 ML 모델 @001 사용 성공!")
                print(f"임베딩 차원: {len(rows2[0]['embedding'])}")
                print(f"임베딩 샘플: {rows2[0]['embedding'][:5]}...")
                return True
            else:
                print("⚠️ 쿼리 2 결과 없음")
                
        except Exception as e:
            print(f"❌ 쿼리 2 실패: {str(e)[:100]}...")
        
        # 방법 3: 다른 모델명 시도
        query3 = """
        SELECT ML.GENERATE_EMBEDDING(
          MODEL `bigquery-public-data.ml_models.textembedding_gecko@latest`,
          'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        try:
            print("쿼리 3 실행 중...")
            result3 = client.query(query3)
            rows3 = list(result3)
            
            if rows3:
                print("🎉 공개 ML 모델 @latest 사용 성공!")
                print(f"임베딩 차원: {len(rows3[0]['embedding'])}")
                print(f"임베딩 샘플: {rows3[0]['embedding'][:5]}...")
                return True
            else:
                print("⚠️ 쿼리 3 결과 없음")
                
        except Exception as e:
            print(f"❌ 쿼리 3 실패: {str(e)[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ 공개 ML 모델 테스트 오류: {str(e)}")
        return False

def test_hacker_news_with_public_model():
    """공개 ML 모델로 해커뉴스 데이터 임베딩 생성 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 공개 ML 모델로 해커뉴스 데이터 임베딩 생성 테스트...")
        
        # 공개 모델로 해커뉴스 데이터 임베딩 생성
        query = """
        SELECT
          id,
          title,
          text,
          ML.GENERATE_EMBEDDING(
            MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
            STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
          ).ml_generate_embedding_result AS embedding
        FROM
          `bigquery-public-data.hacker_news.full`
        WHERE
          title IS NOT NULL OR text IS NOT NULL
        LIMIT 5
        """
        
        try:
            print("해커뉴스 임베딩 쿼리 실행 중...")
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("🎉 공개 ML 모델로 해커뉴스 임베딩 생성 성공!")
                print(f"생성된 임베딩 수: {len(rows)}")
                for i, row in enumerate(rows[:3]):  # 처음 3개만 표시
                    print(f"  {i+1}. ID: {row['id']}, 제목: {row['title'][:50]}...")
                    print(f"     임베딩 차원: {len(row['embedding'])}")
                return True
            else:
                print("⚠️ 해커뉴스 임베딩 결과 없음")
                return False
                
        except Exception as e:
            print(f"❌ 해커뉴스 임베딩 테스트 오류: {str(e)[:100]}...")
            return False
        
    except Exception as e:
        print(f"❌ 해커뉴스 임베딩 테스트 오류: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 공개 ML 모델을 직접 사용하여 ML.GENERATE_EMBEDDING 테스트 시작")
    print("=" * 80)
    
    # 1. 공개 ML 모델 직접 사용 테스트
    public_model_ok = test_public_ml_model_direct()
    
    # 2. 공개 ML 모델로 해커뉴스 데이터 임베딩 생성 테스트
    hacker_news_ok = test_hacker_news_with_public_model()
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 공개 ML 모델 직접 사용 테스트 결과 요약")
    print("=" * 80)
    print(f"공개 ML 모델 직접 사용: {'✅ 성공' if public_model_ok else '❌ 실패'}")
    print(f"해커뉴스 데이터 임베딩: {'✅ 성공' if hacker_news_ok else '❌ 실패'}")
    
    if public_model_ok and hacker_news_ok:
        print("\n🎉 공개 ML 모델 사용 성공! Connection 없이도 ML.GENERATE_EMBEDDING 사용 가능!")
        print("💡 Kaggle 대회 준비 완료! 해커뉴스 데이터로 임베딩 생성 시작!")
        print("💡 다음 단계: 대량 데이터로 임베딩 생성 및 테이블 저장")
    else:
        print("\n🚨 공개 ML 모델 사용에도 실패")
        print("💡 해결방법: BigQuery ML API 권한 문제일 가능성이 높습니다")
        print("💡 GCP 콘솔에서 BigQuery ML 관련 API 활성화가 필요할 수 있습니다")
    
    print("\n🔍 모든 테스트는 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 