import subprocess
import sys
from pathlib import Path

def test_schema_script_exit_zero():
    metrics_file = Path("metrics/axes_run.json")
    if not metrics_file.exists():
        subprocess.run(
            ["nebula-axes-run", "--input", "data/raw/sample.csv", "--out", str(metrics_file)],
            check=True
        )
    result = subprocess.run(
        [sys.executable, "scripts/validate_metrics_schema.py", "--file", str(metrics_file)],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0 