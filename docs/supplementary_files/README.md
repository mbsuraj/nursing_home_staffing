# Supplementary Files

Supporting data and code for the manuscript. Files here are intended to be combined
into a single supplementary PDF at submission.

All data is derived from the public CMS Payroll-Based Journal (PBJ) employee-detail
files. No individual-level or facility-identifying data is included; all values are
aggregated to the state × month × ownership × role level.

---

## `separation_rates_state_month_ownership_role.csv`

The single master aggregate underlying every results statistic. All three findings —
geographic variation, the ownership gradient, and the role differences — roll up from
this one file, so a reviewer can reproduce each number with a simple group-by.

**Population:** Permanent employees (`worker_type = Employee`; contract/agency staff
excluded) in the three direct-care nursing roles (RN, LPN, CNA). Study window:
October 2022 – March 2025 (30 months).

**Grain:** one row per state × month × ownership type × role.

**Columns**

| Column | Description |
|---|---|
| `state` | Two-letter USPS code (includes DC and territories). |
| `month` | Month the values pertain to, labeled by month-start date (`YYYY-MM-01`). |
| `ownership` | Facility ownership: `For-Profit`, `Non-Profit`, or `Government`. |
| `role` | Nursing role: `CNA`, `LPN`, or `RN`. |
| `separation` | Count of permanent employees separating in the month (last working day in month, then 90+ days with no hours at the same facility). |
| `active_headcount` | Count of permanent employees with at least one working day in the month. |
| `separation_rate` | `separation / active_headcount`. |

**How each result rolls up (workforce-weighted = Σ separation / Σ active_headcount):**

- **National monthly rate (~8.2%)** — pool all rows within each month.
- **Annualized turnover (~98%)** — 12 × workforce-weighted monthly rate (flow/stock
  basis; can exceed 100%).
- **Geographic variation** — pool to state × month, then average by state (range ≈ 4.5%
  in HI/DC to > 10% in MO/OK/OH/TX/KS). Persistence test uses the balanced 52-state ×
  30-month matrix (Guam excluded for incomplete coverage): Friedman χ²(51) = 1080,
  p < 0.001; Kendall's W = 0.71.
- **Ownership gradient** — pool to ownership × month. Annualized (12 × monthly):
  For-Profit ≈ 105%, Non-Profit ≈ 77%, Government ≈ 75%. Systematic-difference test on
  state-month blocks with all three ownership types: Friedman χ²(2) = 1633, p < 0.001;
  Kendall's W = 0.56. For-profit highest in every month and 96% of states.
- **Role differences** — monthly rates CNA 8.6%, LPN 7.6%, RN 7.2%. LPN and RN are close
  and not consistently ordered, so they are grouped as licensed nurses and compared with
  CNAs: CNAs higher in every month, all three ownership types, and 85% of states
  (Wilcoxon signed-rank p < 0.001).

**Notes**
- `separation_rate` can be recomputed from `separation / active_headcount`.
- p-values are reported as `p < 0.001`; because state-months are autocorrelated, the
  literal values are optimistic and the conservative threshold is used throughout.

---

## Forecast validation data (external file)

The short-term forecasting result is **not** derived from the master aggregate above;
it comes from the seasonal-naive forecaster output at:

`model/output/seasonal_naive_forecast_rates.csv`

The forecaster (`model/seasonal_naive.py`) predicts each bottom-grain series
(state × ownership × role) as the observed rate in the same calendar month one year
earlier, then forms state / ownership / role / national levels by workforce-weighted
aggregation. Prediction intervals at each level come from that level's in-sample
seasonal-naive residual standard deviation. Rolling-origin robustness is in
`model/rolling_backtest.py` (`rolling_backtest_summary.csv`).

**Columns**

| Column | Description |
|---|---|
| `unique_id` | Series identifier, `state/ownership/role`; the national series is `National/total/total`. |
| `ds` | Forecast month (`YYYY-MM-01`). |
| `forecast` | Point forecast of the monthly separation rate. |
| `forecast_lo80` / `forecast_hi80` | 80% prediction interval bounds. |
| `forecast_lo95` / `forecast_hi95` | 95% prediction interval bounds. |

**Result reproducible from this file (national series, held-out Apr–Jun 2025):**

| Month | Forecast | Observed* | 95% PI |
|---|---|---|---|
| Apr 2025 | 7.25% | 7.14% | 6.4–8.1% |
| May 2025 | 7.71% | 7.55% | 6.9–8.5% |
| Jun 2025 | 8.95% | 8.86% | 8.1–9.8% |

All three held-out months fall within the national prediction interval. *Observed rates
are computed from the panel for the validation months (outside the training window)
using the same workforce-weighted definition.

**Rolling-origin backtest (bottom-grain, workforce-weighted MAE):** across 5 expanding
origins (Mar 2024 – Mar 2025), seasonal-naive averaged 1.24 percentage points vs 1.55 for
a persistence (last-month) baseline, beating persistence at every origin.
