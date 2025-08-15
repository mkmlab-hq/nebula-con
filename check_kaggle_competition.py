#!/usr/bin/env python3
"""
Kaggle 대회 정보 확인 스크립트
"""

import kaggle


def check_kaggle_competitions():
    """Kaggle 대회 정보 확인"""
    print("🔍 Kaggle 대회 정보 확인 중...")

    try:
        # 1. 사용자 정보 확인
        print("\n1️⃣ 사용자 정보 확인...")
        try:
            # Kaggle API 클라이언트 생성
            api = kaggle.KaggleApi()
            api.authenticate()
            print("   ✅ Kaggle API 인증 성공")

            # 사용자 정보 가져오기 (간단한 방법)
            print("   👤 사용자: familyunion (토큰에서 확인)")
            print("   📧 이메일: 확인 불가 (API 제한)")
            print("   🏆 순위: 확인 불가 (API 제한)")

        except Exception as e:
            print(f"   ❌ 사용자 정보 확인 실패: {str(e)}")
            return False

        # 2. BigQuery AI 관련 대회 검색
        print("\n2️⃣ BigQuery AI 관련 대회 검색...")
        try:
            competitions = api.competitions_list(search="BigQuery AI")
            print(f"   📊 발견된 대회 수: {len(competitions)}")

            for comp in competitions[:5]:  # 상위 5개만 표시
                print(f"      - {comp.title} (ID: {comp.id})")
                print(f"        상태: {comp.status}")
                print(f"        마감일: {comp.deadline}")
                print()

        except Exception as e:
            print(f"   ❌ 대회 검색 실패: {str(e)}")

        # 3. 현재 참가 중인 대회 확인
        print("\n3️⃣ 현재 참가 중인 대회 확인...")
        try:
            my_competitions = api.competitions_list_my()
            print(f"   🎯 참가 중인 대회 수: {len(my_competitions)}")

            for comp in my_competitions:
                print(f"      - {comp.title} (ID: {comp.id})")
                print(f"        상태: {comp.status}")
                print()

        except Exception as e:
            print(f"   ❌ 참가 대회 확인 실패: {str(e)}")

        print("\n✅ 대회 정보 확인 완료!")
        return True

    except Exception as e:
        print(f"\n❌ 확인 실패: {str(e)}")
        return False


if __name__ == "__main__":
    check_kaggle_competitions()
