import json
import subprocess
import sys
from pathlib import Path

def run_axes_if_needed():
    axes_file = Path("metrics/axes_run.json")
    if not axes_file.exists():
        # 재생성 (CLI 사용)
        subprocess.run(
            ["nebula-axes-run", "--input", "data/raw/sample.csv", "--out", "metrics/axes_run.json"],
            check=True
        )

def test_threshold_script_runs():
    run_axes_if_needed()
    result = subprocess.run(
        [sys.executable, "scripts/assert_thresholds.py",
         "--metrics", "metrics/axes_run.json",
         "--profile", "config/metrics_profile_default.json"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "Threshold assertion failed"

def test_schema_validation():
    run_axes_if_needed()
    result = subprocess.run(
        [sys.executable, "scripts/validate_metrics_schema.py",
         "--file", "metrics/axes_run.json"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "Schema validation failed"

def test_value_reasonable_ranges():
    run_axes_if_needed()
    data = json.loads(Path("metrics/axes_run.json").read_text(encoding="utf-8"))
    assert 0 <= data["st_var_ratio"] < 3
    assert -1 <= data["seasonal_corr"] <= 1
    assert 0 <= data["psi_trigger_rate"] < 2
    assert 0 <= data["sk_k_score"] < 50
    assert 0 <= data["outlier_impact"] <= 1
    if data.get("dip_stat") is not None:
        assert 0 <= data["dip_stat"] <= 0.3 