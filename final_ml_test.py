#!/usr/bin/env python3
"""
ML.GENERATE_EMBEDDING 기능 최종 테스트
BigQuery AI의 모든 힘을 활용할 수 있는지 확인
"""

from google.cloud import bigquery
from google.api_core import exceptions
import json

def test_ml_generate_embedding():
    """ML.GENERATE_EMBEDDING 함수 최종 테스트"""
    try:
        # BigQuery 클라이언트 생성
        client = bigquery.Client(project='persona-diary-service')
        print("✅ BigQuery 클라이언트 생성 성공")
        print(f"현재 프로젝트: {client.project}")
        
        # 테스트 1: 기본 ML.GENERATE_EMBEDDING 함수 테스트
        print("\n🔍 테스트 1: ML.GENERATE_EMBEDDING 기본 기능 테스트")
        
        query1 = """
        SELECT ML.GENERATE_EMBEDDING(
            MODEL `bigquery-public-data.ml_models.textembedding_gecko`,
            'Hello, this is a test for Kaggle competition'
        ) AS embedding
        """
        
        print("쿼리 실행 중...")
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

def test_alternative_models():
    """대안 모델 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 테스트 2: 대안 모델 테스트")
        
        # 다른 모델명으로 시도
        models_to_test = [
            'bigquery-public-data.ml_models.textembedding_gecko@001',
            'bigquery-public-data.ml_models.textembedding_gecko@latest',
            'bigquery-public-data.ml_models.textembedding_gecko'
        ]
        
        for model in models_to_test:
            try:
                print(f"모델 테스트: {model}")
                query = f"""
                SELECT ML.GENERATE_EMBEDDING(
                    MODEL `{model}`,
                    'Test text for embedding'
                ) AS embedding
                """
                
                result = client.query(query)
                rows = list(result)
                
                if rows:
                    print(f"🎉 모델 {model} 테스트 성공!")
                    return True
                    
            except Exception as e:
                print(f"❌ 모델 {model} 테스트 실패: {str(e)}")
                continue
        
        print("⚠️ 모든 대안 모델 테스트 실패")
        return False
        
    except Exception as e:
        print(f"❌ 대안 모델 테스트 오류: {str(e)}")
        return False

def test_public_dataset_access():
    """공개 데이터셋 접근 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 테스트 3: 공개 데이터셋 접근 테스트")
        
        # 다른 공개 데이터셋으로 테스트
        query = """
        SELECT name, population 
        FROM `bigquery-public-data.utility_us.city` 
        WHERE state = 'CA' 
        LIMIT 3
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ 공개 데이터셋 접근 성공!")
            for row in rows:
                print(f"  - {row['name']}: {row['population']:,}명")
            return True
        else:
            print("⚠️ 공개 데이터셋 결과 없음")
            return False
            
    except Exception as e:
        print(f"❌ 공개 데이터셋 테스트 오류: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 ML.GENERATE_EMBEDDING 기능 최종 테스트 시작")
    print("=" * 60)
    
    # 테스트 실행
    test1_success = test_ml_generate_embedding()
    test2_success = test_alternative_models()
    test3_success = test_public_dataset_access()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 최종 테스트 결과 요약")
    print("=" * 60)
    print(f"ML.GENERATE_EMBEDDING 기본 기능: {'✅ 성공' if test1_success else '❌ 실패'}")
    print(f"대안 모델 테스트: {'✅ 성공' if test2_success else '❌ 실패'}")
    print(f"공개 데이터셋 접근: {'✅ 성공' if test3_success else '❌ 실패'}")
    
    if test1_success or test2_success:
        print("\n🎉 BigQuery ML 기능 사용 가능! Kaggle 대회 준비 완료!")
        print("💡 다음 단계: Hacker News 데이터로 임베딩 생성 및 테이블 저장")
    else:
        print("\n🚨 BigQuery ML API 권한 문제 해결 필요!")
        print("💡 해결방법:")
        print("   1. Google Cloud Console에서 BigQuery ML API 활성화")
        print("   2. 서비스 계정에 'BigQuery ML Admin' 역할 부여")
        print("   3. 또는 다른 임베딩 서비스 사용 (OpenAI, Hugging Face 등)")

if __name__ == "__main__":
    main() 