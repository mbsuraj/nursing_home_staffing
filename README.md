# Nursing Home Workforce Instability

Reproduction materials for a research paper on monthly employee separation (turnover)
in U.S. nursing homes, using CMS Payroll-Based Journal (PBJ) data.

**Purpose of this repository.** It exists solely to **reproduce the results and exhibits**
reported in the manuscript (currently under review at a peer-reviewed health policy
journal). It is not a general-purpose library.

## What the paper shows

Using ~30 months of CMS PBJ employee-detail records (October 2022 – March 2025), the
paper documents that nursing-home turnover follows structured, repeatable patterns —
geographic, ownership-based, role-based, and seasonal (quarter-end) — and that a simple
seasonal-naive model can anticipate near-term, state-level turnover well enough to be
useful for workforce planning.

## Reproduce the results

1. Install dependencies (Python 3.12+):
   ```
   pip install -r requirements.txt
   ```
2. Open and run end-to-end:
   ```
   eda/01_reproduce_paper_results.ipynb
   ```
   This single notebook reproduces every results-section statistic (geographic
   variation, ownership gradient, role differences, quarter-end seasonality), the
   rolling-origin backtest, the forecast validation, and all four exhibits — all from
   `data/panel.csv`.

## Repository layout

```
data/panel.csv                          Analysis input: State × Ownership × Role × Month panel
eda/01_reproduce_paper_results.ipynb    Standalone reproduction of all paper results + exhibits
eda/02_eda_panel.ipynb                  Exploratory panel analysis
eda/03_health_affairs.ipynb             Exploratory / submission-specific analysis
model/seasonal_naive.py                 Seasonal-naive forecaster (bottom grain + weighted roll-up)
model/rolling_backtest.py               Rolling-origin backtest vs a persistence baseline
figures/generate_exhibits.py            Exhibits 2–4
figures/generate_map.py                 Exhibit 1 (state choropleth map)
docs/supplementary_files/               Supplementary data + data dictionary
adhoc_scripts/                          One-off CMS data fetch/validation utilities
```

## Data source

CMS Payroll-Based Journal (PBJ) employee-detail files — public, quarterly release
(data.cms.gov). Only the aggregated `data/panel.csv` is tracked in this repository.
