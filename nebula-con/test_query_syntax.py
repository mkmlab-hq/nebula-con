#!/usr/bin/env python3
"""
BigQuery Remote Model 쿼리 구문 진단 및 수정 테스트
"""


from google.cloud import bigquery


def test_query_syntax():
    """다양한 쿼리 구문을 테스트하여 올바른 구문을 찾습니다."""

    print("🔍 BigQuery Remote Model 쿼리 구문 진단 시작...")

    # BigQuery 클라이언트 생성
    client = bigquery.Client()
    print(f"✅ BigQuery 클라이언트 생성 성공 (프로젝트: {client.project})")

    # 테스트할 쿼리 구문들
    test_queries = [
        {
            "name": "백틱(`) 사용",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`, STRUCT('What is the news about AI?' AS content)) AS embedding"
        },
        {
            "name": "작은따옴표(') 사용",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL 'persona-diary-service.nebula_con_kaggle.text_embedding_remote_model', STRUCT('What is the news about AI?' AS content)) AS embedding"
        },
        {
            "name": "점(.) 대신 언더스코어(_) 사용",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL persona_diary_service.nebula_con_kaggle.text_embedding_remote_model, STRUCT('What is the news about AI?' AS content)) AS embedding"
        },
        {
            "name": "경로 전체를 큰따옴표(\")로 감싸기",
            "query": 'SELECT ML.GENERATE_EMBEDDING(MODEL "persona-diary-service.nebula_con_kaggle.text_embedding_remote_model", STRUCT("What is the news about AI?" AS content)) AS embedding'
        },
        {
            "name": "프로젝트명 생략 (데이터셋.모델명만)",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL `nebula_con_kaggle.text_embedding_remote_model`, STRUCT('What is the news about AI?' AS content)) AS embedding"
        },
        {
            "name": "단순화된 모델명",
            "query": "SELECT ML.GENERATE_EMBEDDING(MODEL text_embedding_remote_model, STRUCT('What is the news about AI?' AS content)) AS embedding"
        }
    ]

    results = []

    for test in test_queries:
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
    print("📊 쿼리 구문 테스트 결과 요약")
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
    test_query_syntax()
