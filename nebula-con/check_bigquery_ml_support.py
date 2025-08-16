#!/usr/bin/env python3
"""
BigQuery ML API 지원 상태 확인 스크립트
사용 가능한 모델 타입과 API 지원 여부를 점검
"""

from google.cloud import bigquery


def check_bigquery_ml_support():
    """BigQuery ML API 지원 상태를 확인합니다."""
    
    print("🔍 BigQuery ML API 지원 상태 확인...")
    
    try:
        client = bigquery.Client()
        
        # 1. 사용 가능한 모델 타입 확인
        print("\n1️⃣ 사용 가능한 모델 타입 확인...")
        
        # 간단한 모델 생성 시도로 지원 여부 확인
        test_queries = [
            # 기본 모델 타입 테스트
            """
            CREATE OR REPLACE MODEL `nebula_con_kaggle.test_model_linear`
            OPTIONS(
                model_type='LINEAR_REG'
            )
            AS SELECT 1 as x, 1 as y
            """,
            
            # 원격 모델 타입 테스트
            """
            CREATE OR REPLACE MODEL `nebula_con_kaggle.test_model_remote`
            OPTIONS(
                model_type='REMOTE_MODEL'
            )
            """,
            
            # 외부 모델 타입 테스트
            """
            CREATE OR REPLACE MODEL `nebula_con_kaggle.test_model_external`
            OPTIONS(
                model_type='EXTERNAL'
            )
            """
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 테스트 쿼리 {i} 실행...")
            print(f"쿼리: {query.strip()}")
            
            try:
                job = client.query(query)
                job.result()
                print(f"✅ 모델 타입 지원됨")
                
                # 테스트 모델 삭제
                if i == 1:
                    client.delete_model("nebula_con_kaggle.test_model_linear")
                    print("🗑️ 테스트 모델 삭제 완료")
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ 모델 타입 미지원: {error_msg}")
                
                # 오류 분석
                if "not a valid value" in error_msg:
                    print("🔍 분석: 해당 모델 타입이 지원되지 않음")
                elif "permission" in error_msg:
                    print("🔍 분석: 권한 문제")
                else:
                    print("🔍 분석: 기타 오류")
        
        # 2. BigQuery ML 함수 지원 확인
        print("\n2️⃣ BigQuery ML 함수 지원 확인...")
        
        ml_functions = [
            "ML.GENERATE_EMBEDDING",
            "ML.PREDICT", 
            "ML.EVALUATE",
            "ML.FEATURE_INFO"
        ]
        
        for func in ml_functions:
            print(f"\n🔍 {func} 함수 테스트...")
            
            if func == "ML.GENERATE_EMBEDDING":
                test_query = f"""
                SELECT {func}(
                    'test text',
                    'textembedding-gecko@003'
                ) AS result
                LIMIT 1
                """
            else:
                test_query = f"""
                SELECT {func}(
                    MODEL `nebula_con_kaggle.test_model_linear`,
                    (SELECT 1 as x)
                ) AS result
                LIMIT 1
                """
            
            try:
                result = client.query(test_query)
                rows = list(result.result())
                print(f"✅ {func} 함수 지원됨")
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ {func} 함수 미지원: {error_msg}")
        
        # 3. BigQuery AI 함수 지원 확인
        print("\n3️⃣ BigQuery AI 함수 지원 확인...")
        
        ai_functions = [
            "AI.GENERATE_TEXT",
            "AI.GENERATE_EMBEDDING",
            "AI.SUMMARIZE_TEXT"
        ]
        
        for func in ai_functions:
            print(f"\n🔍 {func} 함수 테스트...")
            
            test_query = f"""
            SELECT {func}(
                'Hello, how are you?',
                'gemini-pro'
            ) AS result
            LIMIT 1
            """
            
            try:
                result = client.query(test_query)
                rows = list(result.result())
                print(f"✅ {func} 함수 지원됨")
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ {func} 함수 미지원: {error_msg}")
        
        return True
        
    except Exception as e:
        print(f"❌ BigQuery ML API 지원 확인 실패: {str(e)}")
        return False


def suggest_alternatives():
    """BigQuery ML API 미지원 시 대안 방안을 제시합니다."""
    
    print("\n🚨 BigQuery ML API 미지원 시 대안 방안...")
    
    print("\n1️⃣ Vertex AI 직접 호출 방식:")
    print("   - BigQuery ML 함수 대신 Vertex AI Python SDK 사용")
    print("   - textembedding-gecko 모델 직접 호출")
    print("   - gemini-pro 모델 직접 호출")
    
    print("\n2️⃣ 하이브리드 접근법:")
    print("   - BigQuery: 데이터 저장 및 기본 쿼리")
    print("   - Vertex AI: 임베딩 생성 및 AI 답변")
    print("   - Python: 두 서비스 연결 및 조정")
    
    print("\n3️⃣ 키워드 기반 접근법 (현재 구현됨):")
    print("   - AI 모델 없이 키워드 매칭으로 검색")
    print("   - 템플릿 기반 답변 생성")
    print("   - 즉시 실행 가능한 상태")


def main():
    """메인 실행 함수"""
    print("🚨 BigQuery ML API 지원 상태 확인 시작...")
    
    try:
        success = check_bigquery_ml_support()
        
        if success:
            print("\n✅ BigQuery ML API 지원 상태 확인 완료!")
        else:
            print("\n❌ BigQuery ML API 지원 상태 확인 실패!")
        
        suggest_alternatives()
        
        return 0
        
    except Exception as e:
        print(f"❌ 메인 실행 오류: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 