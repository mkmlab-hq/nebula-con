# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Threshold enforcement & CI pipeline
- Performance optimization & caching
- Advanced metrics (Jensen-Shannon divergence, sliding PSI)
- Report generation & visualization

## [0.2.0] - 2025-08-14

### Added
- **Modular core metrics package** (`src/nebula_axes/`)
  - A-axis: Temporal stability (st_var_ratio, seasonal_corr)
  - A-axis: Drift detection (psi_trigger_rate)
  - B-axis: Distributional shape (sk_k_score, outlier_impact, **dip_stat**)
  - C-axis: Semantic density (intra_cluster_density, silhouette_approx, density_k)
  - D-axis: Cross-domain transferability (retention metrics)
- **CLI tools** for easy usage
  - `nebula-axes-run`: Compute axes metrics
  - `nebula-retention-run`: Compute retention metrics
  - `nebula-metrics-full`: Full analysis (axes + retention)
- **Package structure** with proper entry points
- **Development tools**: Makefile + PowerShell script
- **Comprehensive documentation** with Quick Start guide

### Changed
- **B-axis completion**: Added `dip_stat` (Hartigan Dip Test) for unimodality detection
- **Modular architecture**: Separated metrics into logical modules
- **Import structure**: Clean package imports with relative paths

### Fixed
- **Import path issues** in modular structure
- **Edge case handling** for insufficient data samples

### Technical Details
- **Minimum Python version**: 3.8+
- **Dependencies**: numpy, pandas, scikit-learn, scipy
- **Build system**: hatchling
- **Package name**: nebula-axes

## [0.1.0] - 2025-08-14

### Added
- Basic metrics calculation framework
- PSI (Population Stability Index) implementation
- Initial axes metrics (temporal, shape, density)
- Basic data ingestion pipeline

### Known Issues
- Limited modularity
- No CLI interface
- Basic error handling

---

## Version Strategy

- **v0.2.0**: (Current) Packaging + CLI + dip_stat ✅
- **v0.2.1**: Threshold + CI pipeline
- **v0.3.0**: Performance/caching + run_meta + report generation
- **v0.3.1**: Full documentation + overview + methodology
- **v0.4.0**: Advanced metrics (JS divergence, sliding PSI, scenario simulation)

## Migration Guide

### From v0.1.0 to v0.2.0

**Breaking Changes:**
- Import paths changed to use `nebula_axes` package
- CLI commands replace direct Python script execution

**Migration Steps:**
1. Install new package: `pip install -e .`
2. Use CLI commands instead of Python scripts:
   - Old: `python pipelines/dataset_ingest.py --input data.csv`
   - New: `nebula-axes-run --input data.csv`
3. Update import statements in custom code:
   - Old: `from utils.dip import approximate_dip`
   - New: `from nebula_axes.utils.dip import approximate_dip`

**Backward Compatibility:**
- Old scripts remain functional but deprecated
- New modular structure provides better maintainability 