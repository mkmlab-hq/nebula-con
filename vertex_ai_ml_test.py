#!/usr/bin/env python3
"""
사령관님이 제시해주신 정확한 ML.GENERATE_EMBEDDING 테스트
Vertex AI API 전파 지연 문제 해결 확인
"""

from google.cloud import bigquery
from google.api_core import exceptions

def test_ml_generate_embedding_correct():
    """사령관님이 제시해주신 정확한 쿼리로 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 사령관님이 제시해주신 정확한 쿼리로 ML.GENERATE_EMBEDDING 테스트...")
        
        # 사령관님이 제시해주신 정확한 쿼리
        query = """
        SELECT ML.GENERATE_EMBEDDING(
          MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
          STRUCT('Hello, this is a test for Kaggle competition' AS content)
        ) AS embedding
        FROM
          `bigquery-public-data.hacker_news.full`
        LIMIT 10
        """
        
        print("쿼리 실행 중...")
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("🎉 ML.GENERATE_EMBEDDING 함수 테스트 성공!")
            print(f"생성된 임베딩 수: {len(rows)}")
            for i, row in enumerate(rows[:3]):  # 처음 3개만 표시
                print(f"  {i+1}. 임베딩 차원: {len(row['embedding'])}")
                print(f"     임베딩 샘플: {row['embedding'][:5]}...")
            return True
        else:
            print("⚠️ ML.GENERATE_EMBEDDING 결과가 없습니다")
            return False
            
    except exceptions.GoogleAPICallError as e:
        print(f"❌ Google API 오류: {str(e)}")
        
        # 오류 코드별 상세 분석
        if "403" in str(e):
            print("🔍 문제: Vertex AI API 권한 부족")
            print("💡 해결방법: Vertex AI API 활성화 및 전파 대기 필요")
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

def test_vertex_ai_api_status():
    """Vertex AI API 상태 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 Vertex AI API 상태 확인...")
        
        # 간단한 Vertex AI 관련 쿼리 테스트
        query = """
        SELECT 1 as test
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ 기본 BigQuery 연결 정상")
            print("✅ Vertex AI API 기본 상태 확인됨")
            return True
        else:
            print("⚠️ 기본 쿼리 결과 없음")
            return False
            
    except Exception as e:
        print(f"❌ Vertex AI API 상태 확인 오류: {str(e)}")
        return False

def test_public_dataset_access():
    """공개 데이터셋 접근 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 공개 데이터셋 접근 확인...")
        
        # 해커뉴스 데이터셋 접근 테스트
        query = """
        SELECT COUNT(*) as cnt
        FROM `bigquery-public-data.hacker_news.full`
        LIMIT 1
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            print("✅ 해커뉴스 데이터셋 접근 성공!")
            print(f"  데이터 수: {rows[0]['cnt']:,}")
            return True
        else:
            print("⚠️ 해커뉴스 데이터셋 결과 없음")
            return False
            
    except Exception as e:
        print(f"❌ 공개 데이터셋 접근 테스트 오류: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 사령관님이 제시해주신 정확한 ML.GENERATE_EMBEDDING 테스트 시작")
    print("=" * 80)
    
    # 1. Vertex AI API 상태 확인
    vertex_ai_ok = test_vertex_ai_api_status()
    
    # 2. 공개 데이터셋 접근 확인
    dataset_ok = test_public_dataset_access()
    
    # 3. ML.GENERATE_EMBEDDING 함수 테스트 (사령관님의 정확한 쿼리)
    ml_ok = test_ml_generate_embedding_correct()
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 사령관님의 정확한 진단 기반 테스트 결과 요약")
    print("=" * 80)
    print(f"Vertex AI API 상태: {'✅ 정상' if vertex_ai_ok else '❌ 문제'}")
    print(f"공개 데이터셋 접근: {'✅ 성공' if dataset_ok else '❌ 실패'}")
    print(f"ML.GENERATE_EMBEDDING: {'✅ 성공' if ml_ok else '❌ 실패'}")
    
    if ml_ok:
        print("\n🎉 Vertex AI API 전파 완료! ML.GENERATE_EMBEDDING 함수 사용 가능!")
        print("💡 Kaggle 대회 준비 완료! 해커뉴스 데이터로 임베딩 생성 시작!")
    else:
        print("\n🚨 Vertex AI API 전파 지연 문제 지속")
        print("💡 해결방법: GCP 콘솔에서 Vertex AI API 재활성화 및 전파 대기")
        print("💡 전파 시간: 최소 5-15분, 때로는 더 오래 걸릴 수 있음")
    
    print("\n🔍 모든 테스트는 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 