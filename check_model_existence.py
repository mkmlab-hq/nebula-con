#!/usr/bin/env python3
"""
text_embedding_remote_model 존재 여부 확인
사령관님의 정확한 진단 기반 모델 상태 점검
"""

from google.cloud import bigquery
from google.api_core import exceptions

def check_model_existence():
    """text_embedding_remote_model 존재 여부 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 text_embedding_remote_model 존재 여부 확인...")
        
        # 방법 1: INFORMATION_SCHEMA.ML_MODELS에서 확인
        query1 = """
        SELECT model_id, model_type, creation_time
        FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
        WHERE model_id = 'text_embedding_remote_model'
        """
        
        try:
            result1 = client.query(query1)
            rows1 = list(result1)
            
            if rows1:
                print("✅ text_embedding_remote_model 발견!")
                for row in rows1:
                    print(f"  - 모델 ID: {row['model_id']}")
                    print(f"  - 모델 타입: {row['model_type']}")
                    print(f"  - 생성 시간: {row['creation_time']}")
                return True
            else:
                print("⚠️ text_embedding_remote_model이 ML_MODELS에 없습니다")
                
        except Exception as e:
            print(f"❌ ML_MODELS 확인 실패: {str(e)[:100]}...")
        
        # 방법 2: 데이터셋 내 테이블 목록에서 확인
        print("\n🔍 데이터셋 내 테이블 및 모델 목록 확인...")
        try:
            dataset_ref = client.dataset('nebula_con_kaggle', project='persona-diary-service')
            tables = list(client.list_tables(dataset_ref))
            
            print(f"데이터셋 'nebula_con_kaggle' 내 테이블/모델:")
            for table in tables:
                print(f"  - {table.table_id} ({table.table_type})")
                
        except Exception as e:
            print(f"❌ 데이터셋 목록 확인 실패: {str(e)[:100]}...")
        
        # 방법 3: 직접 모델 호출 시도
        print("\n🔍 직접 모델 호출 시도...")
        try:
            query3 = """
            SELECT ML.GENERATE_EMBEDDING(
              MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
              STRUCT('test' AS content)
            ) AS embedding
            """
            
            result3 = client.query(query3)
            rows3 = list(result3)
            
            if rows3:
                print("✅ 직접 모델 호출 성공!")
                return True
            else:
                print("⚠️ 직접 모델 호출 결과 없음")
                
        except Exception as e:
            print(f"❌ 직접 모델 호출 실패: {str(e)[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ 모델 존재 여부 확인 오류: {str(e)}")
        return False

def check_alternative_models():
    """대안 모델 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 사용 가능한 다른 모델 확인...")
        
        # 공개 ML 모델 확인
        query = """
        SELECT model_id, model_type
        FROM `bigquery-public-data.ml_models.__TABLES__`
        WHERE table_id LIKE '%textembedding%'
        LIMIT 10
        """
        
        try:
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("✅ 공개 ML 모델 발견:")
                for row in rows:
                    print(f"  - {row['model_id']}: {row['model_type']}")
                return True
            else:
                print("⚠️ 공개 ML 모델을 찾을 수 없습니다")
                
        except Exception as e:
            print(f"❌ 공개 ML 모델 확인 실패: {str(e)[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ 대안 모델 확인 오류: {str(e)}")
        return False

def main():
    """메인 확인 실행"""
    print("🚀 text_embedding_remote_model 존재 여부 확인 시작")
    print("=" * 80)
    
    # 1. 모델 존재 여부 확인
    model_exists = check_model_existence()
    
    # 2. 대안 모델 확인
    alternative_models = check_alternative_models()
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 모델 존재 여부 확인 결과 요약")
    print("=" * 80)
    print(f"text_embedding_remote_model: {'✅ 존재' if model_exists else '❌ 존재하지 않음'}")
    print(f"대안 모델: {'✅ 발견' if alternative_models else '❌ 발견되지 않음'}")
    
    if not model_exists:
        print("\n🚨 핵심 문제: text_embedding_remote_model이 존재하지 않습니다!")
        print("💡 해결방법:")
        print("   1. 모델을 먼저 생성해야 합니다")
        print("   2. 또는 공개 ML 모델을 사용해야 합니다")
        print("   3. Vertex AI에서 원격 모델을 연결해야 합니다")
    
    print("\n🔍 모든 확인은 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 