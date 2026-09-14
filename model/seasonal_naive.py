"""
Seasonal-naive forecaster for NH employee separation rates.

Method (deliberately simple, fully reproducible):
- Base forecast at the bottom grain (state x ownership x role): the separation rate
  for a target month equals the observed rate in the same calendar month one year
  earlier (a 12-month seasonal-naive forecast). Only pre-cutoff data is used.
- Higher levels (state, ownership, role, national) are formed post hoc by
  workforce-weighted aggregation of the bottom-series forecasts, using each series'
  active headcount at the training cutoff as weights.
- Prediction intervals at every level come from that level's in-sample seasonal-naive
  residual standard deviation (point +/- z*sigma; 80% and 95%). For horizons within
  the 12-month season the seasonal-naive interval width is constant in h.

Output schema matches what the exhibits/notebook consume:
  unique_id, ds, forecast, forecast_lo80, forecast_hi80, forecast_lo95, forecast_hi95
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import norm

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
TRAIN_END_DEFAULT = "2025-03-01"
MIN_AVG_ACTIVE = 30           # series-inclusion threshold (matches prior model)
Z = {"80": norm.ppf(0.90), "95": norm.ppf(0.975)}   # 1.2816, 1.96


def build_bottom():
    """Bottom-grain panel: state x ownership x role x month, thin series dropped."""
    panel = pd.read_csv(DATA_DIR / "panel.csv", parse_dates=["month_end"])
    emp = panel[panel["worker_type"] == "Employee"]
    b = (emp.groupby(["state", "ownership", "role", "month_end"])
         .agg(seps=("separation_count", "sum"), active=("active_count", "sum")).reset_index())
    b["series"] = b.state + "/" + b.ownership + "/" + b.role
    b["rate"] = b.seps / b.active
    keep = b.groupby("series").active.mean()
    keep = keep[keep >= MIN_AVG_ACTIVE].index
    return b[b.series.isin(keep)].copy()


def _nodes(series_list):
    """Enumerate hierarchy nodes as (unique_id, boolean series-mask)."""
    parts = [s.split("/") for s in series_list]
    st = np.array([p[0] for p in parts]); ow = np.array([p[1] for p in parts]); ro = np.array([p[2] for p in parts])
    nodes = [(s, np.arange(len(series_list)) == i) for i, s in enumerate(series_list)]
    for a in np.unique(st):
        for o in np.unique(ow):
            m = (st == a) & (ow == o)
            if m.any(): nodes.append((f"{a}/{o}/total", m))
    for a in np.unique(st):
        for r in np.unique(ro):
            m = (st == a) & (ro == r)
            if m.any(): nodes.append((f"{a}/total/{r}", m))
    for a in np.unique(st):
        nodes.append((f"{a}/total/total", st == a))
    for o in np.unique(ow):
        nodes.append((f"National/{o}/total", ow == o))
    for r in np.unique(ro):
        nodes.append((f"National/total/{r}", ro == r))
    nodes.append(("National/total/total", np.ones(len(series_list), bool)))
    return nodes


def forecast(b, train_end=TRAIN_END_DEFAULT, horizon_end=None):
    """Seasonal-naive forecasts + prediction intervals at every hierarchy level."""
    train_end = pd.Timestamp(train_end)
    series_list = sorted(b.series.unique())
    rate = b.pivot(index="series", columns="month_end", values="rate").reindex(series_list)
    seps = b.pivot(index="series", columns="month_end", values="seps").reindex(series_list).fillna(0)
    active = b.pivot(index="series", columns="month_end", values="active").reindex(series_list).fillna(0)
    w = active[train_end].reindex(series_list).fillna(0).values          # weights at cutoff

    def naive_node(mask, T):
        src = T - pd.DateOffset(months=12)
        if src not in rate.columns:
            return np.nan
        r = rate[src].values
        ww = w * mask * (~np.isnan(r))
        s = ww.sum()
        return np.nan if s == 0 else (ww * np.nan_to_num(r)).sum() / s

    def obs_node(mask, T):
        if T not in seps.columns:
            return np.nan
        am = (active[T].values * mask).sum()
        return np.nan if am == 0 else (seps[T].values * mask).sum() / am

    if horizon_end is None:
        horizon_end = train_end + pd.DateOffset(months=12)
    targets = pd.date_range(train_end + pd.offsets.MonthBegin(1), pd.Timestamp(horizon_end), freq="MS")
    all_months = list(rate.columns)
    hist_targets = [m for m in all_months
                    if (m - pd.DateOffset(months=12)) in rate.columns and m <= train_end]

    records = []
    for uid, mask in _nodes(series_list):
        res = [obs_node(mask, T) - naive_node(mask, T) for T in hist_targets]
        res = [x for x in res if not np.isnan(x)]
        sigma = np.std(res, ddof=1) if len(res) > 1 else np.nan
        for T in targets:
            f = naive_node(mask, T)
            if np.isnan(f):
                continue
            row = {"unique_id": uid, "ds": T, "forecast": min(max(f, 0.0), 1.0)}
            for lvl, z in Z.items():
                row[f"forecast_lo{lvl}"] = max(f - z * sigma, 0.0) if not np.isnan(sigma) else np.nan
                row[f"forecast_hi{lvl}"] = min(f + z * sigma, 1.0) if not np.isnan(sigma) else np.nan
            records.append(row)
    return pd.DataFrame(records)


def main():
    """Generate the seasonal-naive forecast file and print a national summary."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    b = build_bottom()
    fc = forecast(b, TRAIN_END_DEFAULT)
    path = OUTPUT_DIR / "seasonal_naive_forecast_rates.csv"
    fc.to_csv(path, index=False)
    print(f"Wrote {path}: {fc.unique_id.nunique()} series, {len(fc)} rows")
    nat = fc[fc.unique_id == "National/total/total"]
    print(nat[["ds", "forecast", "forecast_lo95", "forecast_hi95"]].head(6).to_string(index=False))
    return fc


if __name__ == "__main__":
    main()
