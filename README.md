# NebulaCon - 4x3 Universal Pattern Axes (UPA)

Mission: Cross-dataset generalization & drift robustness lens (Kaggle/CPGP Tier0Tier3).

## Tier0 Exit (Must):
- axes_registry.json v0.1 with 12 micro axes
- Working ingest  profile JSON
- Baseline macro_f1 logged (metrics/baseline_run.json)
- Axes feature dump (stdout or metrics/axes_sample.json)
- CI green (lint+baseline smoke)

## Axes Implementation Status

| Macro Axis | Micro Axis | Metric | Status |
|------------|------------|--------|--------|
| **A - Temporal Stability** | A1 | st_var_ratio | pending |
| | A2 | seasonal_corr | pending |
| | **A3** | **psi_trigger_rate** | **implemented (PSI)** |
| **B - Distributional Shape** | B1 | sk_k_score | pending |
| | B2 | outlier_impact | pending |
| | B3 | dip_stat | pending |
| **C - Semantic Density** | C1 | intra_cluster_dist | pending |
| | C2 | silhouette | pending |
| | C3 | mutual_info_reduction | pending |
| **D - Cross-Domain Transferability** | D1 | loss_retention_ratio | pending |
| | D2 | steps_to_plateau | pending |
| | D3 | leak_score | pending |
