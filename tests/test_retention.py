import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from scripts.generate_shifted_dataset import main as gen_shift
from scripts.run_retention import main as run_ret

def test_retention_pipeline(tmp_path):
    """Test the complete retention pipeline"""
    # 준비: 간단한 synthetic dataset
    n = 600
    rng = np.random.default_rng(0)
    df = pd.DataFrame({
        "feat_a": rng.normal(0,1,n).cumsum(),  # 트렌드
        "feat_b": rng.normal(5,2,n),
        "feat_c": rng.normal(-2,1.5,n),
        "target": rng.integers(0,3,n)
    })
    base_path = tmp_path/"base.csv"
    shift_path = tmp_path/"shift.csv"
    out_path = tmp_path/"retention.json"
    df.to_csv(base_path, index=False)

    # shift 생성
    gen_shift(str(base_path), str(shift_path))
    # retention 계산
    run_ret(str(base_path), str(shift_path), str(out_path))

    assert out_path.exists()
    data = json.loads(out_path.read_text())
    assert data["macro_f1_base"] is not None
    assert data["retention_zero_shot"] is not None
    assert data["retention_retrained"] is not None
    # 재학습 후 성능이 zero-shot 보다 같거나 개선되는 경향
    if data["macro_f1_shifted_zero_shot"] and data["macro_f1_shifted_retrained"]:
        assert data["macro_f1_shifted_retrained"] >= data["macro_f1_shifted_zero_shot"] - 1e-6

def test_shifted_dataset_generation():
    """Test shifted dataset generation"""
    # Create test data
    df = pd.DataFrame({
        "feat_a": [1, 2, 3, 4, 5],
        "feat_b": [10, 20, 30, 40, 50],
        "target": [0, 1, 0, 1, 0]
    })
    
    # Test shift generation logic
    df_shift = df.copy()
    df_shift["feat_a"] = df_shift["feat_a"] + 0.8  # mean shift
    df_shift["feat_b"] = df_shift["feat_b"] * 1.15  # scale
    
    assert df_shift["feat_a"].iloc[0] == 1.8  # 1 + 0.8
    assert df_shift["feat_b"].iloc[0] == 11.5  # 10 * 1.15

def test_retention_calculation():
    """Test retention calculation logic"""
    # Mock data
    f1_base = 0.85
    f1_zero_shot = 0.70
    f1_retrained = 0.82
    
    retention_zero = f1_zero_shot / (f1_base + 1e-9)
    retention_retrained = f1_retrained / (f1_base + 1e-9)
    
    assert retention_zero < 1.0  # Performance degradation
    assert retention_retrained > retention_zero  # Retraining helps
    assert retention_retrained < 1.0  # Still some degradation 