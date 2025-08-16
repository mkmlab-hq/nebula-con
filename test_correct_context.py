#!/usr/bin/env python3
"""
올바른 프로젝트 컨텍스트에서 ML.GENERATE_EMBEDDING 함수 테스트
프로젝트 컨텍스트 불일치 문제 해결 후 최종 검증
"""

from google.cloud import bigquery
from google.api_core import exceptions

def test_ml_generate_embedding_correct_context():
    """올바른 프로젝트 컨텍스트에서 ML.GENERATE_EMBEDDING 테스트"""
    try:
        # 명시적으로 프로젝트 지정
        client = bigquery.Client(project='persona-diary-service')
        print("✅ BigQuery 클라이언트 생성 성공")
        print(f"현재 프로젝트: {client.project}")
        
        print("\n🔍 ML.GENERATE_EMBEDDING 함수 테스트 시작...")
        
        # 테스트 1: 기본 ML.GENERATE_EMBEDDING 함수
        query1 = """
        SELECT ML.GENERATE_EMBEDDING(
            MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
            'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        print("쿼리 1 실행 중...")
        result1 = client.query(query1)
        rows1 = list(result1)
        
        if rows1:
            print("🎉 ML.GENERATE_EMBEDDING 기본 기능 테스트 성공!")
            print(f"임베딩 차원: {len(rows1[0]['embedding'])}")
            print(f"임베딩 샘플: {rows1[0]['embedding'][:5]}...")
            return True
        else:
            print("⚠️ ML.GENERATE_EMBEDDING 결과가 없습니다")
            return False
            
    except exceptions.GoogleAPICallError as e:
        print(f"❌ Google API 오류: {str(e)}")
        
        # 오류 코드별 상세 분석
        if "403" in str(e):
            print("🔍 문제: BigQuery ML API 권한 부족")
            print("💡 해결방법: Google Cloud Console에서 BigQuery ML API 활성화 필요")
        elif "400" in str(e):
            print("🔍 문제: 쿼리 문법 오류 또는 모델 접근 불가")
            print("💡 해결방법: 모델명 확인 및 문법 검증 필요")
        elif "404" in str(e):
            print("🔍 문제: 모델 또는 데이터셋을 찾을 수 없음")
            print("💡 해결방법: 모델 경로 및 데이터셋 존재 여부 확인 필요")
        
        return False
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        return False

def test_hacker_news_embedding():
    """해커뉴스 데이터로 실제 임베딩 생성 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 해커뉴스 데이터 임베딩 생성 테스트...")
        
        # 실제 해커뉴스 데이터로 임베딩 생성
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
        
        print("해커뉴스 임베딩 쿼리 실행 중...")
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("🎉 해커뉴스 데이터 임베딩 생성 성공!")
            print(f"생성된 임베딩 수: {len(rows)}")
            for i, row in enumerate(rows):
                print(f"  {i+1}. ID: {row['id']}, 제목: {row['title'][:50]}...")
                print(f"     임베딩 차원: {len(row['embedding'])}")
            return True
        else:
            print("⚠️ 해커뉴스 임베딩 결과가 없습니다")
            return False
            
    except Exception as e:
        print(f"❌ 해커뉴스 임베딩 테스트 오류: {str(e)}")
        return False

def test_own_model_access():
    """자체 모델 접근 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 자체 모델 접근 테스트...")
        
        # 자체 데이터셋의 모델 확인
        query = """
        SELECT model_id, model_type, creation_time
        FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
        LIMIT 10
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ 자체 ML 모델 확인 성공!")
            for row in rows:
                print(f"  - {row['model_id']}: {row['model_type']}")
            return True
        else:
            print("⚠️ 자체 ML 모델이 없습니다")
            return False
            
    except Exception as e:
        print(f"❌ 자체 모델 접근 테스트 오류: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 올바른 프로젝트 컨텍스트에서 ML.GENERATE_EMBEDDING 테스트 시작")
    print("=" * 70)
    
    # 1. 기본 ML.GENERATE_EMBEDDING 함수 테스트
    test1_success = test_ml_generate_embedding_correct_context()
    
    # 2. 해커뉴스 데이터 임베딩 생성 테스트
    test2_success = test_hacker_news_embedding()
    
    # 3. 자체 모델 접근 테스트
    test3_success = test_own_model_access()
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("📊 프로젝트 컨텍스트 수정 후 최종 테스트 결과")
    print("=" * 70)
    print(f"ML.GENERATE_EMBEDDING 기본 기능: {'✅ 성공' if test1_success else '❌ 실패'}")
    print(f"해커뉴스 데이터 임베딩: {'✅ 성공' if test2_success else '❌ 실패'}")
    print(f"자체 모델 접근: {'✅ 성공' if test3_success else '❌ 실패'}")
    
    if test1_success and test2_success:
        print("\n🎉 프로젝트 컨텍스트 문제 해결 성공!")
        print("💡 BigQuery ML 기능 사용 가능! Kaggle 대회 준비 완료!")
        print("💡 다음 단계: 대량 데이터로 임베딩 생성 및 테이블 저장")
    else:
        print("\n🚨 여전히 문제가 있습니다")
        print("💡 추가 진단이 필요합니다")
    
    print("\n🔍 모든 테스트는 실제 BigQuery 쿼리 실행 기반입니다")

if __name__ == "__main__":
    main() 