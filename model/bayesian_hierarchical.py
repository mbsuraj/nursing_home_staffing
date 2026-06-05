"""
Bayesian Hierarchical Model: NH Employee Separation Rates

Structure:
- Local level (random walk) per State×Role — captures slow trend/drift
- 12-month seasonality — partially pooled across series
- Hierarchical priors — small states borrow strength from national

rate_{s,r,t} = level_{s,r,t} + seasonal_{s,r,month(t)} + ε
level_{s,r,t} = level_{s,r,t-1} + drift_{s,r,t}

Priors:
- level_{s,r,0} ~ Normal(μ_national, σ_level)
- drift_{s,r,t} ~ Normal(0, σ_drift)  [shared σ_drift across series]
- seasonal_{s,r,m} ~ Normal(γ_m, σ_seasonal)  [pooled toward national seasonal]
- σ_obs ~ HalfNormal

Train: Oct 2022 – Jun 2025 (33 months)
Validate: Jul – Sep 2025 (3 months)
Forecast: 6 months ahead
"""

import pandas as pd
import numpy as np
import os
os.environ["PYTENSOR_FLAGS"] = "device=cpu,floatX=float64,cxx="
import pymc as pm
import arviz as az
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

TRAIN_START, TRAIN_END = "2022-10-01", "2025-03-01"
VAL_START, VAL_END = "2025-04-01", "2025-06-01"
HORIZON = 21  # Apr 2025 through Dec 2026 = 21 months
N_SAMPLES = 1000
N_TUNE = 1000


# ─── 1. Build panel ──────────────────────────────────────────────────────────
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
    bottom["series"] = bottom["state"] + "/" + bottom["ownership"] + "/" + bottom["role"]

    # Drop thin series
    avg_active = bottom.groupby("series")["active"].mean()
    keep = avg_active[avg_active >= 30].index
    bottom = bottom[bottom["series"].isin(keep)].copy()

    # Create series index
    series_list = sorted(bottom["series"].unique())
    series_map = {s: i for i, s in enumerate(series_list)}
    bottom["series_idx"] = bottom["series"].map(series_map)

    # Time index
    all_months = sorted(bottom["month_end"].unique())
    month_map = {m: i for i, m in enumerate(all_months)}
    bottom["t"] = bottom["month_end"].map(month_map)

    # Calendar month (0-11)
    bottom["cal_month"] = bottom["month_end"].dt.month - 1

    # Weights for roll-up
    weights = (
        bottom[bottom["month_end"] == pd.Timestamp(TRAIN_END)]
        .set_index("series")["active"]
        .to_dict()
    )

    print(f"Series: {len(series_list)}, Months: {len(all_months)}")
    return bottom, series_list, all_months, weights


# ─── 2. Fit Bayesian model ───────────────────────────────────────────────────
def fit_model(train_df, n_series, n_months):
    """
    Bayesian hierarchical structural time series:
    - Partially pooled local level
    - Partially pooled 12-month seasonality
    """
    series_idx = train_df["series_idx"].values
    t_idx = train_df["t"].values
    cal_month = train_df["cal_month"].values
    y = train_df["rate"].values

    with pm.Model() as model:
        # --- Hyperpriors ---
        mu_level = pm.Normal("mu_level", mu=0.08, sigma=0.03)
        sigma_level = pm.HalfNormal("sigma_level", sigma=0.03)
        sigma_drift = pm.HalfNormal("sigma_drift", sigma=0.005)
        sigma_obs = pm.HalfNormal("sigma_obs", sigma=0.02)

        # Seasonal hyperpriors (national-level monthly pattern)
        gamma = pm.Normal("gamma", mu=0, sigma=0.02, shape=12)
        sigma_seasonal = pm.HalfNormal("sigma_seasonal", sigma=0.01)

        # --- Series-level parameters ---
        # Initial level per series (pooled toward national mean)
        level_init = pm.Normal("level_init", mu=mu_level, sigma=sigma_level, shape=n_series)

        # Level drift (random walk innovations) — shared variance
        drift = pm.Normal("drift", mu=0, sigma=sigma_drift, shape=(n_series, n_months - 1))

        # Build level paths: level[:,t] = level[:,t-1] + drift[:,t-1]
        level = pm.math.concatenate([
            level_init.reshape((n_series, 1)),
            level_init.reshape((n_series, 1)) + pm.math.cumsum(drift, axis=1)
        ], axis=1)

        # Seasonal effect per series (pooled toward national gamma)
        seasonal = pm.Normal("seasonal", mu=gamma, sigma=sigma_seasonal, shape=(n_series, 12))

        # --- Likelihood ---
        mu = level[series_idx, t_idx] + seasonal[series_idx, cal_month]
        pm.Normal("obs", mu=mu, sigma=sigma_obs, observed=y)

    with model:
        trace = pm.sample(N_SAMPLES, tune=N_TUNE, cores=2, random_seed=42,
                          target_accept=0.9, return_inferencedata=True)

    return model, trace


# ─── 3. Forecast ──────────────────────────────────────────────────────────────
def forecast(trace, n_series, n_train_months, horizon=HORIZON):
    """
    Generate posterior-predictive forecasts as a full sample array.

    For each posterior draw, the latent level is propagated forward as a proper
    random walk: level_{T+k} = level_T + sum of k independent N(0, sigma_drift)
    increments, using that draw's own sigma_drift. Seasonal effect and one
    observation-noise draw are added per step. This yields coherent trajectories
    whose spread widens with horizon as sqrt(k) and correctly propagates posterior
    uncertainty in sigma_drift and sigma_obs.

    Returns array of shape (samples, series, horizon).
    """
    post = trace.posterior
    level_init = post["level_init"].values.reshape(-1, n_series)        # (S, series)
    drift = post["drift"].values.reshape(-1, n_series, n_train_months - 1)
    seasonal = post["seasonal"].values.reshape(-1, n_series, 12)         # (S, series, 12)
    sigma_drift = post["sigma_drift"].values.reshape(-1)                 # (S,) global scalar
    sigma_obs = post["sigma_obs"].values.reshape(-1)                     # (S,)
    n_samples = level_init.shape[0]

    # Latent level at end of training = init + cumulative training drift
    level = level_init + drift.sum(axis=2)  # (S, series)

    forecasts = np.zeros((n_samples, n_series, horizon))
    rng = np.random.default_rng(42)

    for h in range(horizon):
        # Calendar month: first training month is Oct 2022 (index 9, 0-based)
        cal_m = (9 + n_train_months + h) % 12

        # One random-walk increment per step, using each draw's own sigma_drift
        level = level + rng.normal(0.0, 1.0, size=(n_samples, n_series)) * sigma_drift[:, None]

        # Observed rate = level + seasonal + observation noise
        obs_noise = rng.normal(0.0, 1.0, size=(n_samples, n_series)) * sigma_obs[:, None]
        forecasts[:, :, h] = level + seasonal[:, :, cal_m] + obs_noise

    return forecasts  # (samples, series, horizon)


# ─── 4. Summarize and roll up ─────────────────────────────────────────────────
def summarize_forecasts(forecasts, series_list, all_months, weights, train_end_idx):
    """
    Compute point forecasts (median) and prediction intervals at every hierarchy
    level. Aggregation to higher levels is done at the SAMPLE level — taking the
    workforce-weighted average of each posterior sample across the relevant series,
    then computing percentiles. This correctly accounts for error cancellation
    across series (diversification), unlike averaging precomputed quantiles.
    """
    from pandas.tseries.offsets import MonthBegin

    n_samples, n_ser, horizon = forecasts.shape
    last_train = all_months[train_end_idx]
    forecast_dates = pd.date_range(last_train + MonthBegin(1), periods=horizon, freq="MS")

    # Parse dimensions and weights per bottom-level series
    parts = [s.split("/") for s in series_list]
    states = np.array([p[0] for p in parts])
    owns = np.array([p[1] for p in parts])
    roles = np.array([p[2] for p in parts])
    w = np.array([weights.get(s, 0.0) for s in series_list])  # (series,)

    def summarize_group(uid, mask):
        """Weighted-average the samples across masked series, return summary rows."""
        gw = w[mask]
        tw = gw.sum()
        if tw <= 0:
            return []
        # Weighted mean rate per (sample, horizon): sum_i w_i * rate / sum_i w_i
        sub = forecasts[:, mask, :]                          # (S, n_in_group, H)
        rolled = np.tensordot(gw, sub, axes=([0], [1])) / tw  # (S, H)
        rolled = np.clip(rolled, 0, 1)
        rows = []
        for h in range(horizon):
            col = rolled[:, h]
            rows.append({
                "unique_id": uid,
                "ds": forecast_dates[h],
                "BayesHier": np.median(col),
                "BayesHier-lo-80": np.percentile(col, 10),
                "BayesHier-hi-80": np.percentile(col, 90),
                "BayesHier-lo-95": np.percentile(col, 2.5),
                "BayesHier-hi-95": np.percentile(col, 97.5),
            })
        return rows

    records = []

    # Bottom level: State/Ownership/Role (each series on its own)
    for i, uid in enumerate(series_list):
        mask = np.zeros(n_ser, dtype=bool)
        mask[i] = True
        records.extend(summarize_group(uid, mask))

    # State x Ownership (across roles)
    for st in np.unique(states):
        for ow in np.unique(owns):
            mask = (states == st) & (owns == ow)
            if mask.any():
                records.extend(summarize_group(f"{st}/{ow}/total", mask))

    # State x Role (across ownership)
    for st in np.unique(states):
        for ro in np.unique(roles):
            mask = (states == st) & (roles == ro)
            if mask.any():
                records.extend(summarize_group(f"{st}/total/{ro}", mask))

    # State (all)
    for st in np.unique(states):
        records.extend(summarize_group(f"{st}/total/total", states == st))

    # Ownership (national)
    for ow in np.unique(owns):
        records.extend(summarize_group(f"National/{ow}/total", owns == ow))

    # Role (national)
    for ro in np.unique(roles):
        records.extend(summarize_group(f"National/total/{ro}", roles == ro))

    # National
    records.extend(summarize_group("National/total/total", np.ones(n_ser, dtype=bool)))

    return pd.DataFrame(records)


# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BAYESIAN HIERARCHICAL MODEL: NH Separation Rates")
    print("=" * 60)

    print("\n1. Building panel...")
    bottom, series_list, all_months, weights = build_panel()
    n_series = len(series_list)

    # Split
    train = bottom[(bottom["month_end"] >= TRAIN_START) & (bottom["month_end"] <= TRAIN_END)]
    val = bottom[(bottom["month_end"] >= VAL_START) & (bottom["month_end"] <= VAL_END)]
    n_train_months = train["t"].nunique()
    train_end_idx = train["t"].max()
    print(f"   Train: {n_train_months} months, Val: {val['month_end'].nunique()} months")
    print(f"   Series: {n_series}")

    print("\n2. Fitting Bayesian model (this may take a few minutes)...")
    model, trace = fit_model(train, n_series, n_train_months)
    print("   Done.")

    # Save trace
    import pickle
    trace_path = OUTPUT_DIR / "bayesian_trace.pkl"
    with open(trace_path, "wb") as f:
        pickle.dump({"trace": trace, "series_list": series_list, "n_train_months": n_train_months,
                     "train_end_idx": train_end_idx, "weights": weights}, f)
    print(f"   Model saved to {trace_path}")

    # Diagnostics
    print("\n3. Diagnostics...")
    summary = az.summary(trace, var_names=["mu_level", "sigma_level", "sigma_drift", "sigma_obs", "sigma_seasonal"])
    print(summary.to_string())

    print("\n4. Forecasting...")
    fcst_samples = forecast(trace, n_series, n_train_months, HORIZON)
    results = summarize_forecasts(fcst_samples, series_list, all_months, weights, train_end_idx)
    print(f"   {results['unique_id'].nunique()} series, {results.shape[0]} rows")

    # Evaluate
    print("\n5. Validation...")
    val_rates = val[["series", "month_end", "rate", "active"]].rename(
        columns={"series": "unique_id", "month_end": "ds", "rate": "y"}
    )
    eval_df = results.merge(val_rates, on=["unique_id", "ds"], how="inner")
    if not eval_df.empty:
        err = eval_df["BayesHier"] - eval_df["y"]
        mae = err.abs().mean()
        wmape = (err.abs() * eval_df["active"]).sum() / (eval_df["y"].abs() * eval_df["active"]).sum()
        print(f"   MAE:   {mae:.5f}")
        print(f"   wMAPE: {wmape:.1%} (workforce-weighted)")

    # Save
    results.to_csv(OUTPUT_DIR / "bayesian_forecast_rates.csv", index=False)

    # Save in-sample fitted values
    print("\n6. Computing in-sample fitted values...")
    level = trace.posterior["level_init"].values  # (chain, draw, series)
    drift = trace.posterior["drift"].values  # (chain, draw, series, T-1)
    seasonal = trace.posterior["seasonal"].values  # (chain, draw, series, 12)

    # Flatten chains and take posterior mean
    level_init_mean = level.reshape(-1, n_series).mean(axis=0)
    drift_mean = drift.reshape(-1, n_series, n_train_months - 1).mean(axis=0)
    seasonal_mean = seasonal.reshape(-1, n_series, 12).mean(axis=0)

    # Build level path: level[s, t] = init[s] + cumsum(drift[s, :t])
    level_path = np.zeros((n_series, n_train_months))
    level_path[:, 0] = level_init_mean
    for t in range(1, n_train_months):
        level_path[:, t] = level_init_mean + drift_mean[:, :t].sum(axis=1)

    # Fitted = level + seasonal
    fitted_records = []
    train_sorted = train.sort_values(["series_idx", "t"])
    for _, row in train_sorted.iterrows():
        s_idx = int(row["series_idx"])
        t_idx = int(row["t"])
        cal_m = int(row["cal_month"])
        fitted_val = level_path[s_idx, t_idx] + seasonal_mean[s_idx, cal_m]
        fitted_records.append({
            "unique_id": row["series"],
            "ds": row["month_end"],
            "actual": row["rate"],
            "fitted": np.clip(fitted_val, 0, 1),
        })

    fitted_df = pd.DataFrame(fitted_records)
    fitted_df.to_csv(OUTPUT_DIR / "bayesian_fitted_values.csv", index=False)
    print(f"   Fitted values: {fitted_df.shape}")

    # National summary
    nat = results[results["unique_id"] == "National/total/total"][["unique_id", "ds", "BayesHier", "BayesHier-lo-80", "BayesHier-hi-80"]]
    print(f"\n   National forecasts:\n{nat.to_string(index=False)}")
    print("\nDone.")
