# Metrics Threshold & CI Enforcement Guide

## Purpose
Automated guardrails to detect regression, extreme values and structural breaks in Tier0 metrics.

## Files
- `config/metrics_profile_default.json`: Declarative min/max + warn_above + allow_none
- `scripts/assert_thresholds.py`: Hard validation (exit 1 on violation)
- `scripts/validate_metrics_schema.py`: Pydantic schema shape guard
- `tests/test_thresholds.py`: Pytest integration
- `.github/workflows/metrics-ci.yaml`: CI pipeline

## Policy
| Metric | Range | Warn | None? | Rationale |
|--------|-------|------|-------|-----------|
| st_var_ratio | [0,3) | - | No | Rolling/global variance sanity |
| seasonal_corr | [-1,1] | - | No | Autocorr bounds |
| psi_trigger_rate | [0,2) | >0.7 | No | PSI rarely >1; warn early |
| sk_k_score | [0,50) | - | No | Combined shape stability |
| outlier_impact | [0,1] | - | No | Fraction clamp |
| dip_stat | [0,0.3] | - | Yes | Multi-modality approx cap |
| intra_cluster_density | [0,5] | - | Yes | Normalized dispersion |
| silhouette_approx | [-1,1] | - | Yes | Standard range |
| density_k | [2,20] | - | Yes | K search sanity |

## Escalation
- Threshold violation (error) → CI fail
- Warn_above triggered → log warning (optionally fail with --fail-on-warn)
- Schema drift (missing required field) → CI fail

## Extending
1. Add metric entry in profile.
2. Update schema model if required field.
3. Add test assertion.

## Local Run
```bash
nebula-axes-run --input data/raw/sample.csv --out metrics/axes_run.json
python scripts/validate_metrics_schema.py --file metrics/axes_run.json
python scripts/validate_metrics_schema.py --file metrics/axes_run.json
python scripts/assert_thresholds.py --metrics metrics/axes_run.json --profile config/metrics_profile_default.json
pytest -k thresholds -q
``` 