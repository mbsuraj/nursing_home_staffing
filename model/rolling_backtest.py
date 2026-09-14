"""
Rolling-origin backtest of the seasonal-naive forecaster.

Expanding-window origins in the confirmed historical period (targets have a full
90-day separation-confirmation window and a 12-month lag). At each origin we forecast
the next H months and compare two simple methods at the bottom grain
(state x ownership x role), workforce-weighted:

  seasonal_naive : rate = same calendar month one year earlier
  persistence    : rate = last observed (cutoff) month, carried forward

The persistence baseline is a reference showing the seasonal structure matters;
seasonal-naive should beat it because turnover has a strong quarter-end pattern.

Outputs:
  model/output/rolling_backtest_summary.csv  (per origin + pooled, workforce-weighted MAE)
  model/output/rolling_backtest_detail.csv
"""
import numpy as np
import pandas as pd
from seasonal_naive import build_bottom, OUTPUT_DIR

ORIGINS = ["2024-03-01", "2024-06-01", "2024-09-01", "2024-12-01", "2025-03-01"]
H = 3


def main():
    b = build_bottom()
    rate = b.pivot(index="series", columns="month_end", values="rate")
    active = b.pivot(index="series", columns="month_end", values="active")

    rows = []
    for origin in ORIGINS:
        origin = pd.Timestamp(origin)
        for T in pd.date_range(origin + pd.offsets.MonthBegin(1), periods=H, freq="MS"):
            src = T - pd.DateOffset(months=12)
            if src not in rate.columns or T not in rate.columns or origin not in rate.columns:
                continue
            for s in rate.index:
                o, a = rate.at[s, T], active.at[s, T]
                if pd.isna(o) or pd.isna(a):
                    continue
                rows.append({"origin": str(origin.date()), "series": s, "ds": T,
                             "obs": o, "active": a,
                             "snaive": rate.at[s, src], "persist": rate.at[s, origin]})
    d = pd.DataFrame(rows).dropna(subset=["snaive", "persist"])

    def wmae(g, col):
        return np.average((g[col] - g.obs).abs(), weights=g.active)

    summ = []
    for origin, g in list(d.groupby("origin")) + [("POOLED", d)]:
        summ.append({"origin": origin, "n": len(g),
                     "seasonal_naive_wMAE_pp": wmae(g, "snaive") * 100,
                     "persistence_wMAE_pp": wmae(g, "persist") * 100})
    summ = pd.DataFrame(summ)

    d.to_csv(OUTPUT_DIR / "rolling_backtest_detail.csv", index=False)
    summ.to_csv(OUTPUT_DIR / "rolling_backtest_summary.csv", index=False)
    print(summ.to_string(index=False))
    print("\nDone.")


if __name__ == "__main__":
    main()
