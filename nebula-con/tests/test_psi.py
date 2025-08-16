import random

from utils.psi import population_stability_index


def test_psi_positive_when_shifted():
    random.seed(0)
    baseline = [random.gauss(0, 1) for _ in range(600)]
    current = [x + 0.5 for x in baseline]  # 분포 shift
    psi = population_stability_index(baseline, current)
    assert psi > 0, f"Expected psi > 0, got {psi}"


def test_psi_zero_same_values():
    baseline = [1.0] * 120
    current = [1.0] * 150
    psi = population_stability_index(baseline, current)
    assert psi == 0.0


def test_psi_small_samples_returns_zero():
    baseline = [1, 2, 3, 4, 5]
    current = [1, 2, 3, 4, 5, 6]
    psi = population_stability_index(baseline, current, min_samples=50)
    assert psi == 0.0


def test_psi_with_nan_and_none():
    baseline = [1, 2, None, 3, float("nan"), 4] * 30
    current = [1.2, 2.1, None, 3.2, float("nan"), 3.9] * 30
    psi = population_stability_index(baseline, current)
    # 정리 후 길이 충분 → psi 계산 (>=0)
    assert psi >= 0
