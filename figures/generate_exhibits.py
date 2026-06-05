"""
Generate high-DPI exhibits for Health Affairs paper.

Exhibit arc follows the Results narrative:
  Part 1 (instability is patterned):
    Exhibit 1 — State map (geographic variation)        [generate_map.py]
    Exhibit 2 — Ownership comparison over time
  Part 2 (instability is anticipatable):
    Exhibit 3 — National forecast vs observed
    Exhibit 4 — State-level forecast vs observed

Supplementary candidates: ranked state bar, role comparison, quarterly pattern.
All saved to figures/ at 300 DPI.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({
    "font.size": 10, "font.family": "sans-serif",
    "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "model" / "output"
FIG_DIR = Path(__file__).parent

panel = pd.read_csv(DATA_DIR / "panel.csv", parse_dates=["month_end"])
emp = panel[panel["worker_type"] == "Employee"]
hist = emp.groupby(["state", "ownership", "role", "month_end"]).agg(
    active=("active_count", "sum"), seps=("separation_count", "sum")
).reset_index()
hist["rate"] = hist["seps"] / hist["active"]

bayes = pd.read_csv(OUTPUT_DIR / "bayesian_forecast_rates.csv", parse_dates=["ds"])

TRAIN_END = "2025-03-01"
VAL_END = "2025-06-01"

C_FP, C_NP, C_GOV = "#9b2335", "#2c5f8a", "#5b9bd5"
C_OBS, C_FCST = "#2c5f8a", "#9b2335"


# ─── Exhibit 2: Ownership comparison (historical) ────────────────────────────
def exhibit2_ownership():
    train = hist[hist["month_end"] <= TRAIN_END]
    # Workforce-weighted average rate per ownership over full training period
    own = train.groupby("ownership").apply(
        lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
    )
    order = ["For-Profit", "Non-Profit", "Government"]
    own = own.reindex(order)
    colors = {"For-Profit": C_FP, "Non-Profit": C_NP, "Government": C_GOV}

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ann = 1 - (1 - own.values) ** 12  # annualize
    bars = ax.bar(order, ann * 100, color=[colors[o] for o in order],
                  alpha=0.85, width=0.6)
    # Value labels on bars
    for b, v in zip(bars, ann):
        ax.text(b.get_x() + b.get_width() / 2, v * 100 + 0.8, f"{v*100:.0f}%",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylabel("Annualized Employee Separation Rate (%)")
    ax.set_title("Exhibit 2: Annualized Employee Separation Rate by Facility Ownership,\nOctober 2022–March 2025")
    ax.set_ylim(0, max(ann) * 100 * 1.15)
    ax.grid(True, alpha=0.2, axis="y")
    fig.savefig(FIG_DIR / "exhibit2_ownership.png")
    plt.close()
    print("  exhibit2_ownership.png (bar chart)")


# ─── Exhibit 3: National forecast vs observed ────────────────────────────────
def exhibit3_national_forecast():
    DISPLAY_START = "2024-01-01"
    nat_hist = hist[(hist["month_end"] >= DISPLAY_START) & (hist["month_end"] <= VAL_END)].groupby("month_end").apply(
        lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
    ).reset_index(name="rate")
    nat_fcst = bayes[(bayes["unique_id"] == "National/total/total") & (bayes["ds"] <= VAL_END)]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(nat_hist["month_end"], nat_hist["rate"] * 100, "o-", markersize=4,
            color=C_OBS, linewidth=1.3, label="Observed")
    ax.plot(nat_fcst["ds"], nat_fcst["BayesHier"] * 100, "D-", markersize=6,
            color=C_FCST, linewidth=1.6, label="Forecast")
    ax.fill_between(nat_fcst["ds"], nat_fcst["BayesHier-lo-80"] * 100,
                    nat_fcst["BayesHier-hi-80"] * 100, alpha=0.2, color=C_FCST,
                    label="80% prediction interval")
    ax.axvline(pd.Timestamp(TRAIN_END), color="gray", linestyle="--", alpha=0.6,
               linewidth=0.9, label="Training cutoff")
    ax.set_ylabel("Monthly Separation Rate (%)")
    ax.set_title("Exhibit 3: National Forecast vs Observed Separation Rate,\nApril–June 2025")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(5, 11)
    fig.savefig(FIG_DIR / "exhibit3_national_forecast.png")
    plt.close()
    print("  exhibit3_national_forecast.png")


# ─── Exhibit 4: State-level forecast vs observed ─────────────────────────────
def exhibit4_state_forecast():
    high_risk = ["MO", "OK", "TX"]
    low_risk = ["NY"]
    states = high_risk + low_risk

    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharey=True)
    for idx, st in enumerate(states):
        ax = axes[idx // 2, idx % 2]
        sh = hist[hist["state"] == st].groupby("month_end").apply(
            lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
        ).reset_index(name="rate")
        sh = sh[(sh["month_end"] >= "2024-04-01") & (sh["month_end"] <= VAL_END)]
        sf = bayes[(bayes["unique_id"] == f"{st}/total/total") & (bayes["ds"] <= VAL_END)]

        ax.plot(sh["month_end"], sh["rate"] * 100, "o-", markersize=3,
                color=C_OBS, linewidth=1, label="Observed")
        if not sf.empty:
            ax.plot(sf["ds"], sf["BayesHier"] * 100, "D-", markersize=4,
                    color=C_FCST, linewidth=1.2, label="Forecast")
            ax.fill_between(sf["ds"], sf["BayesHier-lo-80"] * 100,
                            sf["BayesHier-hi-80"] * 100, alpha=0.15, color=C_FCST)
        ax.axvline(pd.Timestamp(TRAIN_END), color="gray", linestyle="--",
                   alpha=0.5, linewidth=0.7)
        label = "(high-risk)" if st in high_risk else "(lower-risk)"
        ax.set_title(f"{st} {label}", fontsize=9)
        ax.grid(True, alpha=0.2)
        if idx == 0:
            ax.legend(fontsize=7, loc="upper left")

    fig.suptitle("Exhibit 4: State-Level Forecast vs Observed Separation Rate,\nApril–June 2025",
                 fontsize=11, y=1.02)
    fig.supylabel("Monthly Separation Rate (%)", fontsize=9)
    plt.tight_layout()
    fig.savefig(FIG_DIR / "exhibit4_state_forecast.png")
    plt.close()
    print("  exhibit4_state_forecast.png")


# ─── Supplementary candidates ────────────────────────────────────────────────
def supp_state_bar():
    train = hist[hist["month_end"] <= TRAIN_END]
    sr = train.groupby("state").apply(
        lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
    ).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [C_FP if r > 0.09 else C_NP if r > 0.06 else C_GOV for r in sr.values]
    ax.bar(range(len(sr)), sr.values * 100, color=colors, alpha=0.85)
    ax.set_xticks(range(len(sr)))
    ax.set_xticklabels(sr.index, rotation=90, fontsize=6)
    ax.axhline(sr.mean() * 100, color="black", linestyle="--", linewidth=0.8,
               alpha=0.5, label=f"National average ({sr.mean()*100:.1f}%)")
    ax.set_ylabel("Average Monthly Separation Rate (%)")
    ax.set_title("Supplementary: Separation Rate by State (ranked)")
    ax.legend()
    ax.grid(True, alpha=0.2, axis="y")
    fig.savefig(FIG_DIR / "supp_state_bar.png")
    plt.close()
    print("  supp_state_bar.png")


def supp_roles():
    train = hist[hist["month_end"] <= TRAIN_END]
    rm = train.groupby(["role", "month_end"]).apply(
        lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
    ).reset_index(name="rate")
    colors = {"CNA": C_FP, "LPN": C_NP, "RN": C_GOV}
    fig, ax = plt.subplots(figsize=(8, 4))
    for r in ["CNA", "LPN", "RN"]:
        d = rm[rm["role"] == r]
        ax.plot(d["month_end"], d["rate"] * 100, "o-", markersize=3,
                color=colors[r], linewidth=1.3, label=r)
    ax.set_ylabel("Monthly Separation Rate (%)")
    ax.set_title("Supplementary: Separation Rate by Nursing Role")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.2)
    fig.savefig(FIG_DIR / "supp_roles.png")
    plt.close()
    print("  supp_roles.png")


if __name__ == "__main__":
    print("Generating exhibits (300 DPI)...")
    print("Exhibit 1 (state map): run generate_map.py")
    exhibit2_ownership()
    exhibit3_national_forecast()
    exhibit4_state_forecast()
    print("Supplementary:")
    supp_state_bar()
    supp_roles()
    print("\nDone. Figures saved to figures/")
