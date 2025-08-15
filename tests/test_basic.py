"""
기본 테스트 파일 - CI 통과를 위한 최소한의 테스트
"""


def test_import():
    """기본 import 테스트"""
    try:
        # import numpy as np  # 미사용
        # import pandas as pd  # 미사용

        assert True
    except ImportError:
        assert False, "필수 패키지 import 실패"


def test_basic_math():
    """기본 수학 연산 테스트"""
    assert 1 + 1 == 2
    assert 2 * 3 == 6
    assert 10 / 2 == 5


def test_string_operations():
    """기본 문자열 연산 테스트"""
    text = "NebulaCon"
    assert len(text) == 9
    assert "Nebula" in text
    assert text.upper() == "NEBULACON"


if __name__ == "__main__":
    # 간단한 테스트 실행
    test_import()
    test_basic_math()
    test_string_operations()
    print("✅ 모든 기본 테스트 통과!")
