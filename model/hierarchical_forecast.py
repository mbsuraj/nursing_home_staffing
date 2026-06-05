"""
Hierarchical Forecasting: NH Employee Separation Rates

Strategy: Forecast separation RATES at State×Ownership×Role level,
then roll up using weighted averages (weights = last training month active counts).

Base forecasts: AutoETS(season_length=12)
Benchmark: SeasonalNaive(season_length=12)

Train: Oct 2022 – Mar 2025 (30 months)
Validate: Apr – Jun 2025 (3 months)
"""

import pandas as pd
import numpy as np
from pathlib import Path

from statsforecast import StatsForecast
from statsforecast.models import AutoETS, SeasonalNaive

# ─── Config ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

TRAIN_START, TRAIN_END = "2022-10-01", "2025-03-01"
VAL_START, VAL_END = "2025-04-01", "2025-06-01"
HORIZON = 6
SEASON = 12
LEVELS = [80, 95]
MIN_ACTIVE = 30  # minimum avg active to include a series


# ─── 1. Build bottom-level rate panel ────────────────────────────────────────
def build_panel():
    """Load employee panel, compute State×Ownership×Role×Month rates."""
    panel = pd.read_csv(DATA_DIR / "panel.csv", parse_dates=["month_end"])
    emp = panel[panel["worker_type"] == "Employee"]

    bottom = (
        emp.groupby(["state", "ownership", "role", "month_end"])
        .agg(active=("active_count", "sum"), seps=("separation_count", "sum"))
        .reset_index()
    )
    bottom["rate"] = bottom["seps"] / bottom["active"]
    bottom["unique_id"] = bottom["state"] + "/" + bottom["ownership"] + "/" + bottom["role"]

    # Drop thin series
    avg_active = bottom.groupby("unique_id")["active"].mean()
    keep = avg_active[avg_active >= MIN_ACTIVE].index
    bottom = bottom[bottom["unique_id"].isin(keep)].copy()

    # Weights: last training month active count
    weights = (
        bottom[bottom["month_end"] == TRAIN_END]
        .set_index("unique_id")["active"]
        .to_dict()
    )

    df = bottom[["unique_id", "month_end", "rate", "active", "state", "ownership", "role"]].rename(
        columns={"month_end": "ds", "rate": "y"}
    )

    states = sorted(df["state"].unique())
    ownerships = sorted(df["ownership"].unique())
    roles = sorted(df["role"].unique())
    print(f"States: {len(states)}, Ownerships: {len(ownerships)}, Roles: {len(roles)}")
    print(f"Viable series: {df['unique_id'].nunique()}")

    return df, weights, states, ownerships, roles


# ─── 2. Forecast rates at bottom level ───────────────────────────────────────
def forecast_rates(train_df):
    """Fit AutoETS + SeasonalNaive on State×Ownership×Role rates."""
    sf = StatsForecast(
        models=[AutoETS(season_length=SEASON), SeasonalNaive(season_length=SEASON)],
        freq="MS",
        n_jobs=1,
    )
    df = train_df[["unique_id", "ds", "y"]].copy()
    forecasts = sf.forecast(df=df, h=HORIZON, level=LEVELS)
    if forecasts.index.name == "unique_id":
        forecasts = forecasts.reset_index()
    return forecasts


# ─── 3. Roll up to higher levels ─────────────────────────────────────────────
def roll_up(forecasts, weights, states, ownerships, roles):
    """Weighted average roll-up to all hierarchy levels."""
    pt_cols = [c for c in forecasts.columns
               if c not in ["unique_id", "ds"] and "-lo-" not in c and "-hi-" not in c]

    fcst = forecasts.copy()
    fcst["w"] = fcst["unique_id"].map(weights).fillna(0)
    # Parse dimensions
    parts = fcst["unique_id"].str.split("/", expand=True)
    fcst["state"], fcst["ownership"], fcst["role"] = parts[0], parts[1], parts[2]

    results = [fcst[["unique_id", "ds"] + pt_cols].copy()]

    def weighted_agg(group, label):
        records = []
        for ds, g in group.groupby("ds"):
            tw = g["w"].sum()
            row = {"unique_id": label if callable(label) is False else label(g), "ds": ds}
            for col in pt_cols:
                row[col] = (g[col] * g["w"]).sum() / tw if tw > 0 else 0
            records.append(row)
        return records

    rollup = []

    # State×Ownership
    for (s, o), g in fcst.groupby(["state", "ownership"]):
        for ds, gg in g.groupby("ds"):
            tw = gg["w"].sum()
            row = {"unique_id": f"{s}/{o}/total", "ds": ds}
            for col in pt_cols:
                row[col] = (gg[col] * gg["w"]).sum() / tw if tw > 0 else 0
            rollup.append(row)

    # State×Role
    for (s, r), g in fcst.groupby(["state", "role"]):
        for ds, gg in g.groupby("ds"):
            tw = gg["w"].sum()
            row = {"unique_id": f"{s}/total/{r}", "ds": ds}
            for col in pt_cols:
                row[col] = (gg[col] * gg["w"]).sum() / tw if tw > 0 else 0
            rollup.append(row)

    # State
    for s, g in fcst.groupby("state"):
        for ds, gg in g.groupby("ds"):
            tw = gg["w"].sum()
            row = {"unique_id": f"{s}/total/total", "ds": ds}
            for col in pt_cols:
                row[col] = (gg[col] * gg["w"]).sum() / tw if tw > 0 else 0
            rollup.append(row)

    # Ownership
    for o, g in fcst.groupby("ownership"):
        for ds, gg in g.groupby("ds"):
            tw = gg["w"].sum()
            row = {"unique_id": f"National/{o}/total", "ds": ds}
            for col in pt_cols:
                row[col] = (gg[col] * gg["w"]).sum() / tw if tw > 0 else 0
            rollup.append(row)

    # Role
    for r, g in fcst.groupby("role"):
        for ds, gg in g.groupby("ds"):
            tw = gg["w"].sum()
            row = {"unique_id": f"National/total/{r}", "ds": ds}
            for col in pt_cols:
                row[col] = (gg[col] * gg["w"]).sum() / tw if tw > 0 else 0
            rollup.append(row)

    # National
    for ds, g in fcst.groupby("ds"):
        tw = g["w"].sum()
        row = {"unique_id": "National/total/total", "ds": ds}
        for col in pt_cols:
            row[col] = (g[col] * g["w"]).sum() / tw if tw > 0 else 0
        rollup.append(row)

    results.append(pd.DataFrame(rollup))
    return pd.concat(results, ignore_index=True)


# ─── 4. Evaluate ─────────────────────────────────────────────────────────────
def evaluate(rates_df, val_df, train_df):
    """Compute MAE, workforce-weighted wMAPE, MASE on validation set."""
    pt_cols = [c for c in rates_df.columns
               if c not in ["unique_id", "ds"] and "-lo-" not in c and "-hi-" not in c]

    eval_df = rates_df.merge(val_df[["unique_id", "ds", "y", "active"]], on=["unique_id", "ds"], how="inner")
    if eval_df.empty:
        print("   No validation overlap.")
        return

    # MASE denominator
    naive_resids = []
    for uid, grp in train_df.groupby("unique_id"):
        r = grp.sort_values("ds")["y"].values
        if len(r) > SEASON:
            naive_resids.extend(np.abs(r[SEASON:] - r[:-SEASON]))
    naive_mae = np.mean(naive_resids) if naive_resids else 1.0

    print(f"   Validation points: {len(eval_df)}")
    print(f"   {'Model':<40s} {'MAE':>8s} {'wMAPE':>8s} {'MASE':>8s}")
    print(f"   {'-'*68}")
    for col in pt_cols:
        if col in eval_df.columns:
            err = eval_df[col] - eval_df["y"]
            mae = err.abs().mean()
            # Workforce-weighted wMAPE
            wmape = (err.abs() * eval_df["active"]).sum() / (eval_df["y"].abs() * eval_df["active"]).sum()
            mase = mae / naive_mae
            print(f"   {col:<40s} {mae:>8.5f} {wmape:>7.1%} {mase:>8.3f}")


# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("HIERARCHICAL FORECAST: NH Employee Separation Rates")
    print("=" * 60)

    print("\n1. Building panel...")
    df, weights, states, ownerships, roles = build_panel()

    # Split
    train = df[(df["ds"] >= TRAIN_START) & (df["ds"] <= TRAIN_END)]
    val = df[(df["ds"] >= VAL_START) & (df["ds"] <= VAL_END)]
    print(f"   Train: {train['ds'].nunique()} months, Val: {val['ds'].nunique()} months")

    print("\n2. Forecasting rates...")
    forecasts = forecast_rates(train)
    print(f"   {forecasts.shape}")

    print("\n3. Rolling up...")
    rates = roll_up(forecasts, weights, states, ownerships, roles)
    print(f"   {rates['unique_id'].nunique()} series, {rates.shape[0]} rows")

    print("\n4. Validation...")
    evaluate(rates, val, train)

    # Save
    rates.to_csv(OUTPUT_DIR / "forecast_rates.csv", index=False)

    # National summary
    nat = rates[rates["unique_id"] == "National/total/total"][["unique_id", "ds", "AutoETS", "SeasonalNaive"]]
    print(f"\n   National rate forecasts:\n{nat.to_string(index=False)}")
    print("\nDone.")
