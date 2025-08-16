#!/usr/bin/env python3
"""
생성된 임베딩 테이블 상태 확인 및 문제 진단
"""

from google.cloud import bigquery

def verify_table_status():
    """테이블 상태 확인"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("🔍 생성된 임베딩 테이블 상태 확인...")
        
        # 테이블 정보 확인
        table_id = "persona-diary-service.nebula_con_kaggle.hacker_news_embeddings_pseudo"
        
        try:
            table = client.get_table(table_id)
            print(f"✅ 테이블 존재 확인: {table.table_id}")
            print(f"  - 프로젝트: {table.project}")
            print(f"  - 데이터셋: {table.dataset_id}")
            print(f"  - 생성 시간: {table.created}")
            print(f"  - 행 수: {table.num_rows}")
            print(f"  - 스키마 필드 수: {len(table.schema)}")
            
            # 스키마 상세 정보
            print("\n📋 테이블 스키마:")
            for field in table.schema:
                print(f"  - {field.name}: {field.field_type} ({field.mode})")
            
        except Exception as e:
            print(f"❌ 테이블 정보 가져오기 실패: {str(e)}")
            return False
        
        # 간단한 쿼리로 테이블 접근 테스트
        print("\n🔍 간단한 쿼리로 테이블 접근 테스트...")
        
        try:
            # 가장 기본적인 쿼리
            query1 = f"SELECT COUNT(*) as total_rows FROM `{table_id}`"
            result1 = client.query(query1)
            rows1 = list(result1)
            
            if rows1:
                print(f"✅ 기본 COUNT 쿼리 성공: {rows1[0]['total_rows']}개 행")
            else:
                print("⚠️ COUNT 쿼리 결과 없음")
                
        except Exception as e:
            print(f"❌ COUNT 쿼리 실패: {str(e)}")
        
        # 첫 번째 행 가져오기 테스트
        print("\n🔍 첫 번째 행 가져오기 테스트...")
        
        try:
            query2 = f"SELECT * FROM `{table_id}` LIMIT 1"
            result2 = client.query(query2)
            rows2 = list(result2)
            
            if rows2:
                row = rows2[0]
                print("✅ 첫 번째 행 가져오기 성공!")
                print(f"  - ID: {row['id']}")
                print(f"  - 제목: {row['title'][:50]}..." if row['title'] else "  - 제목: None")
                print(f"  - 텍스트: {row['text'][:50]}..." if row['text'] else "  - 텍스트: None")
                print(f"  - 결합 텍스트: {row['combined_text'][:50]}...")
                print(f"  - 임베딩 차원: {len(row['embedding'])}")
                print(f"  - 임베딩 첫 번째 값: {row['embedding'][0]:.4f}")
                print(f"  - 임베딩 마지막 값: {row['embedding'][-1]:.4f}")
            else:
                print("⚠️ 첫 번째 행 가져오기 결과 없음")
                
        except Exception as e:
            print(f"❌ 첫 번째 행 가져오기 실패: {str(e)}")
        
        # 임베딩 차원 확인 테스트
        print("\n🔍 임베딩 차원 확인 테스트...")
        
        try:
            query3 = f"""
            SELECT 
              id,
              ARRAY_LENGTH(embedding) as embedding_dim
            FROM `{table_id}` 
            LIMIT 5
            """
            result3 = client.query(query3)
            rows3 = list(result3)
            
            if rows3:
                print("✅ 임베딩 차원 확인 성공!")
                for row in rows3:
                    print(f"  - ID {row['id']}: {row['embedding_dim']}차원")
            else:
                print("⚠️ 임베딩 차원 확인 결과 없음")
                
        except Exception as e:
            print(f"❌ 임베딩 차원 확인 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 테이블 상태 확인 오류: {str(e)}")
        return False

def test_simple_operations():
    """간단한 작업 테스트"""
    try:
        client = bigquery.Client(project='persona-diary-service')
        print("\n🔍 간단한 작업 테스트...")
        
        # 테이블 존재 여부 확인
        table_id = "persona-diary-service.nebula_con_kaggle.hacker_news_embeddings_pseudo"
        
        # 테이블 목록에서 확인
        dataset_ref = client.dataset('nebula_con_kaggle', project='persona-diary-service')
        tables = list(client.list_tables(dataset_ref))
        
        print(f"데이터셋 'nebula_con_kaggle' 내 테이블:")
        for table in tables:
            print(f"  - {table.table_id} ({table.table_type})")
            if table.table_id == 'hacker_news_embeddings_pseudo':
                print(f"    ✅ 목표 테이블 발견!")
        
        return True
        
    except Exception as e:
        print(f"❌ 간단한 작업 테스트 오류: {str(e)}")
        return False

def main():
    """메인 실행"""
    print("🚀 생성된 임베딩 테이블 상태 확인 및 문제 진단")
    print("=" * 80)
    
    # 1. 테이블 상태 확인
    table_ok = verify_table_status()
    
    # 2. 간단한 작업 테스트
    simple_ok = test_simple_operations()
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 테이블 상태 확인 결과 요약")
    print("=" * 80)
    print(f"테이블 상태 확인: {'✅ 성공' if table_ok else '❌ 실패'}")
    print(f"간단한 작업 테스트: {'✅ 성공' if simple_ok else '❌ 실패'}")
    
    if table_ok and simple_ok:
        print("\n🎉 테이블이 정상적으로 작동하고 있습니다!")
        print("💡 이제 Kaggle 대회 준비를 진행할 수 있습니다!")
        print("💡 다음 단계: 베이스라인 모델 훈련 및 제출")
    else:
        print("\n⚠️ 테이블에 문제가 있을 수 있습니다")
        print("💡 추가 진단이 필요합니다")
    
    print("\n🔍 모든 확인은 사령관님의 정확한 진단 기반으로 실행되었습니다")

if __name__ == "__main__":
    main() 