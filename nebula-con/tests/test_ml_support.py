#!/usr/bin/env python3
"""
BigQuery ML 기능 지원 여부 확인
"""

from google.cloud import bigquery


def test_ml_support():
    """BigQuery ML 함수가 지원되는지 확인합니다."""

    print("🔍 BigQuery ML 기능 지원 확인 중...")

    # BigQuery 클라이언트 생성
    client = bigquery.Client()
    print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {client.project})")

    # 간단한 ML 함수 테스트
    test_queries = [
        {
            "name": "ML.GENERATE_EMBEDDING 기본 테스트",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL text_embedding_remote_model, 'test') AS embedding"
        },
        {
            "name": "ML.PREDICT 기본 테스트",
            "query": "SELECT ML.PREDICT(MODEL text_embedding_remote_model, STRUCT('test' AS content)) AS prediction"
        }
    ]

    for test in test_queries:
        print(f"\n🔍 {test['name']} 중...")
        print(f"쿼리: {test['query']}")

        try:
            result = client.query(test['query'])
            rows = list(result)
            print("✅ 성공! BigQuery ML 함수 지원됨")
            print(f"결과: {len(rows)}개 행")

        except Exception as e:
            error_msg = str(e)
            print(f"❌ 실패: {error_msg}")

            # 오류 분석
            if "ML.GENERATE_EMBEDDING" in error_msg:
                print("🔍 분석: ML.GENERATE_EMBEDDING 함수가 지원되지 않음")
            elif "MODEL" in error_msg:
                print("🔍 분석: MODEL 키워드 구문 오류")
            else:
                print("🔍 분석: 기타 BigQuery ML 관련 오류")

if __name__ == "__main__":
    test_ml_support()
