#!/usr/bin/env python3
"""
BigQuery ML 공식 문서 기반 구문 테스트
"""

from google.cloud import bigquery


def test_official_syntax():
    """공식 문서의 구문을 기반으로 테스트합니다."""

    print("🔍 BigQuery ML 공식 문서 기반 구문 테스트 시작...")

    # BigQuery 클라이언트 생성
    client = bigquery.Client()
    print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {client.project})")

    # 공식 문서 기반 테스트 쿼리들
    official_queries = [
        {
            "name": "공식 문서 기본 구문 (백틱 + 전체 경로)",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        },
        {
            "name": "STRUCT 없이 직접 텍스트 전달",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        },
        {
            "name": "모델명만 사용 (현재 데이터셋 기준)",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        },
        {
            "name": "데이터셋.모델명 사용",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `nebula_con_kaggle.text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        },
        {
            "name": "ml_generate_embedding 함수 (소문자)",
            "query": "SELECT ml_generate_embedding(MODEL `text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        },
        {
            "name": "AI.GENERATE_EMBEDDING 함수",
            "query": "SELECT AI.GENERATE_EMBEDDING(MODEL `text_embedding_remote_model`, 'What is the news about AI?') AS embedding"
        }
    ]

    results = []

    for test in official_queries:
        print(f"\n🔍 {test['name']} 테스트 중...")
        print(f"쿼리: {test['query']}")

        try:
            result = client.query(test['query'])
            # 결과를 실제로 가져오기
            rows = list(result)
            print(f"✅ 성공! 결과: {len(rows)}개 행")
            if rows:
                print(f"첫 번째 결과: {rows[0]}")
            results.append({
                "name": test['name'],
                "status": "성공",
                "query": test['query'],
                "result_count": len(rows)
            })

        except Exception as e:
            error_msg = str(e)
            print(f"❌ 실패: {error_msg}")
            results.append({
                "name": test['name'],
                "status": "실패",
                "query": test['query'],
                "error": error_msg
            })

    # 결과 요약
    print("\n" + "="*60)
    print("📊 공식 문서 기반 구문 테스트 결과 요약")
    print("="*60)

    success_count = sum(1 for r in results if r['status'] == '성공')
    print(f"성공: {success_count}개, 실패: {len(results) - success_count}개")

    for result in results:
        status_emoji = "✅" if result['status'] == '성공' else "❌"
        print(f"{status_emoji} {result['name']}: {result['status']}")
        if result['status'] == '실패':
            print(f"   오류: {result['error']}")

    return results


if __name__ == "__main__":
    test_official_syntax()
