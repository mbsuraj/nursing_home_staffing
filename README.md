# Nursing Home Workforce Instability: Early Warning Systems

Forecasting monthly nursing home employee separation rates at the state level using CMS Payroll-Based Journal data.

## Overview

This project examines whether routinely collected federal payroll data can support anticipatory workforce planning for U.S. nursing homes. Using 30 months of CMS PBJ employee-detail records (Oct 2022–Mar 2025) covering ~1 million workers across 51 states, we:

1. Measure monthly separation rates by state, ownership type, and nursing role
2. Identify structured patterns (geographic variation, ownership gradient, quarterly periodicity)
3. Demonstrate that these patterns are forecastable using a Bayesian hierarchical model

## Structure

```
data/             Panel dataset (State × Ownership × Role × Month)
model/            Forecasting models (AutoETS baseline + Bayesian hierarchical)
eda/              Exploratory analysis notebooks (pre- and post-forecast)
figures/          Publication-quality exhibits (300 DPI)
docs/             Paper draft and research notes
```

## Workflow

1. **Panel construction** — Raw PBJ quarterly files processed into `data/panel.csv` (State × Ownership × Role × Worker Type × Month)
2. **Pre-model EDA** — `eda/eda_panel.ipynb`: separation rates by worker type, role, ownership, state; seasonal patterns; train/val split design
3. **Modeling** — `model/hierarchical_forecast.py` (AutoETS baseline) and `model/bayesian_hierarchical.py` (Bayesian hierarchical, primary model)
4. **Post-model EDA** — `eda/eda_post_forecasts.ipynb`: forecast vs actual comparisons, error diagnostics, model fit visualization
5. **Exhibits** — `figures/generate_exhibits.py` and `figures/generate_map.py`: publication-ready figures for the paper
6. **Paper** — `docs/paper.md`: draft manuscript targeting Health Affairs ("Building Early Warning Systems for Nursing Home Workforce Instability")

## Key Findings

- Monthly separation rates range from 4–13% across states (threefold spread)
- For-profit facilities: ~66% annualized turnover vs ~53% in government facilities
- Predictable quarter-end spikes (~1.6pp uplift every 3rd month)
- Bayesian hierarchical model achieves 9.3% workforce-weighted prediction error on held-out data

## Data Source

CMS Payroll-Based Journal employee-detail files (public, quarterly release).

## Requirements

Python 3.12+ with: `pandas`, `numpy`, `matplotlib`, `statsforecast`, `hierarchicalforecast`, `pymc`, `geopandas`
