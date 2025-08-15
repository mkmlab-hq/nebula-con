# 4x3 Universal Pattern Axes Specification v0.1

## Scope
Define canonical 4 macro axes + 3 micro feature bundles for cross-domain pattern recognition.

## Canonical Macro Axes

### 1. Activation Axis
**Purpose**: Energy/volatility/burstiness patterns
**Micro Features**:
- \olling_vol_7d\: 7-day rolling volatility
- \ntropy\: Shannon entropy of values
- \urstiness\: Peak-to-mean ratio

### 2. Stability Axis
**Purpose**: Autocorrelation/low-variance/persistence
**Micro Features**:
- \utocorr_lag1\: First-order autocorrelation
- \low_var_ratio\: Variance below threshold ratio
- \persistence_score\: Trend persistence measure

### 3. Directionality Axis
**Purpose**: Forward-looking/innovation/growth semantics
**Micro Features**:
- \uture_term_ratio\: Future-oriented term frequency
- \innovation_score\: Novelty embedding distance
- \growth_trend\: Linear regression slope

### 4. Conservation Axis
**Purpose**: Resource retention/accumulation/drift-resistance
**Micro Features**:
- \esource_retention\: Value preservation ratio
- \ccumulation_rate\: Cumulative growth rate
- \drift_resistance\: Stability against perturbations
