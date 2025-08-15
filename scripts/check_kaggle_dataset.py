#!/usr/bin/env python3
"""
캐글 대회 데이터셋 경로 확인
"""

from google.cloud import bigquery


def check_kaggle_dataset():
    """캐글 대회 데이터셋 경로 확인"""
    print("🔍 캐글 대회 데이터셋 경로 확인...")

    try:
        # 1. BigQuery 클라이언트 초기화
        print("\n1️⃣ BigQuery 클라이언트 초기화...")
        client = bigquery.Client()
        project_id = client.project
        print(f"   ✅ 프로젝트: {project_id}")

        # 2. 일반적인 공개 데이터셋 테스트
        print("\n2️⃣ 일반적인 공개 데이터셋 테스트...")

        test_datasets = [
            "bigquery-public-data.utility_us.city",
            "bigquery-public-data.wikipedia.pageviews_2024",
            "bigquery-public-data.samples.shakespeare",
            "bigquery-public-data.samples.natality",
            "bigquery-public-data.samples.gsod",
        ]

        accessible_datasets = []

        for dataset_path in test_datasets:
            try:
                # 간단한 쿼리로 접근 테스트
                test_query = f"SELECT 1 as test FROM `{dataset_path}` LIMIT 1"
                test_job = client.query(test_query)
                test_job.result()

                print(f"   ✅ 접근 가능: {dataset_path}")
                accessible_datasets.append(dataset_path)

                # 스키마 정보 확인
                try:
                    schema_query = f"SELECT * FROM `{dataset_path}` LIMIT 0"
                    schema_job = client.query(schema_query)
                    schema_job.result()

                    # 테이블 정보 가져오기
                    table_ref = client.get_table(dataset_path)
                    print(f"      📊 행 수: {table_ref.num_rows:,}")
                    print(f"      📋 컬럼 수: {len(table_ref.schema)}")

                    # 텍스트 컬럼 찾기
                    text_columns = []
                    for field in table_ref.schema:
                        if field.field_type == "STRING":
                            text_columns.append(field.name)

                    if text_columns:
                        print(f"      📝 텍스트 컬럼: {', '.join(text_columns[:5])}")
                    else:
                        print("      ⚠️ 텍스트 컬럼 없음")

                except Exception as e:
                    print(f"      ⚠️ 스키마 확인 실패: {str(e)[:50]}...")

            except Exception as e:
                print(f"   ❌ 접근 불가: {dataset_path} - {str(e)[:50]}...")

        # 3. 결과 요약
        print("\n3️⃣ 결과 요약...")
        print(f"   📊 접근 가능한 데이터셋: {len(accessible_datasets)}개")

        if accessible_datasets:
            print("   📋 사용 가능한 데이터셋:")
            for dataset in accessible_datasets:
                print(f"      - {dataset}")

            print("\n   💡 권장사항:")
            print("      1. 위 데이터셋 중 하나를 선택하여 임베딩 생성")
            print("      2. 텍스트 컬럼이 있는 데이터셋 우선 선택")
            print("      3. 행 수가 적당한 데이터셋 선택 (1000-10000행)")
        else:
            print("   ⚠️ 접근 가능한 공개 데이터셋이 없습니다")
            print("   📋 대안:")
            print("      1. 자체 테스트 데이터로 계속 진행")
            print("      2. 캐글 대회 페이지에서 정확한 데이터셋 경로 확인")
            print("      3. BigQuery 콘솔에서 직접 데이터셋 탐색")

        return accessible_datasets

    except Exception as e:
        print(f"\n❌ 데이터셋 확인 실패: {str(e)}")
        print(f"   에러 타입: {type(e).__name__}")
        return []


if __name__ == "__main__":
    check_kaggle_dataset()
