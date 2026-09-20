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
    # Annualize on the flow/stock basis (12 x monthly rate), matching the national
    # turnover figure. This is a separation-event rate and can exceed 100%.
    ann = own.values * 12
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
    fig.text(0.5, 0.01,
             "Notes: Annualized separation events per position (12 × monthly separation rate), consistent with the\n"
             "national turnover definition. Because positions can turn over more than once a year, the rate can exceed 100%.",
             ha="center", va="bottom", fontsize=7, color="#444444")
    fig.subplots_adjust(bottom=0.18)
    fig.savefig(FIG_DIR / "exhibit2_ownership.png")
    plt.close()
    print("  exhibit2_ownership.png (bar chart)")


# ─── Exhibit 3: National forecast vs observed ────────────────────────────────
def exhibit3_national_forecast():
    DISPLAY_START = "2024-01-01"
    nat_hist = hist[(hist["month_end"] >= DISPLAY_START) & (hist["month_end"] <= VAL_END)].groupby("month_end").apply(
        lambda g: g["seps"].sum() / g["active"].sum(), include_groups=False
    ).reset_index(name="rate")
    fcst = pd.read_csv(OUTPUT_DIR / "seasonal_naive_forecast_rates.csv", parse_dates=["ds"])
    nat_fcst = fcst[(fcst["unique_id"] == "National/total/total") & (fcst["ds"] <= VAL_END)]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(nat_hist["month_end"], nat_hist["rate"] * 100, "o-", markersize=4,
            color=C_OBS, linewidth=1.3, label="Observed")
    ax.plot(nat_fcst["ds"], nat_fcst["forecast"] * 100, "D-", markersize=6,
            color=C_FCST, linewidth=1.6, label="Forecast")
    ax.fill_between(nat_fcst["ds"], nat_fcst["forecast_lo80"] * 100,
                    nat_fcst["forecast_hi80"] * 100, alpha=0.2, color=C_FCST,
                    label="80% prediction interval")
    ax.axvline(pd.Timestamp(TRAIN_END), color="gray", linestyle="--", alpha=0.6,
               linewidth=0.9, label="Training cutoff")
    ax.set_ylabel("Monthly Separation Rate (%)")
    ax.set_title("Exhibit 3: National Forecast vs Observed Separation Rate,\nApril–June 2025 Holdout")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(5, 11)
    fig.savefig(FIG_DIR / "exhibit3_national_forecast.png")
    plt.close()
    print("  exhibit3_national_forecast.png")


# ─── Exhibit 4: State risk quadrant (forecasted rate × workforce size) ────────
def exhibit4_state_forecast():
    """Scatter: forecasted separation rate vs workforce size, by state."""
    # Get forecasted rate (avg over validation period) per state
    fcst = pd.read_csv(OUTPUT_DIR / "seasonal_naive_forecast_rates.csv", parse_dates=["ds"])
    state_fcst = fcst[fcst["unique_id"].str.match(r"^[A-Z]{2}/total/total$")].copy()
    state_fcst["state"] = state_fcst["unique_id"].str[:2]
    state_fcst = state_fcst[state_fcst["ds"] <= VAL_END]
    state_avg_rate = state_fcst.groupby("state")["forecast"].mean()

    # Get workforce size (last training month active count per state)
    train = pd.read_csv(DATA_DIR / "panel.csv", parse_dates=["month_end"])
    emp_train = train[(train["worker_type"] == "Employee") & (train["month_end"] == TRAIN_END)]
    state_size = emp_train.groupby("state")["active_count"].sum()

    # Merge
    df = pd.DataFrame({"rate": state_avg_rate, "size": state_size}).dropna()
    # Exclude WV for readability: forecast 18.6%, ~7,400 employees. Its forecast reflects
    # a non-recurring June 2024 separation spike (33.9% that month, a facility-level event)
    # projected forward by the seasonal method; WV's actual 2025 rate returned to ~7%.
    df = df.drop(index="WV", errors="ignore")
    df["rate_pct"] = df["rate"] * 100

    # Quadrant thresholds
    rate_med = df["rate_pct"].median()
    size_med = df["size"].median()

    fig, ax = plt.subplots(figsize=(8.5, 6))

    # Shade quadrants
    xlim = (0, df["size"].max() / 1000 * 1.1)
    ylim = (df["rate_pct"].min() * 0.9, df["rate_pct"].max() * 1.05)
    ax.axhspan(rate_med, ylim[1], xmin=0, xmax=1, alpha=0.04, color=C_FCST)
    ax.axhspan(ylim[0], rate_med, xmin=0, xmax=1, alpha=0.04, color=C_OBS)

    # Plot states as small dots + text labels with minor manual offsets for readability
    for state, row in df.iterrows():
        color = C_FCST if row["rate_pct"] >= rate_med else C_OBS
        weight = "bold" if state in ["OK", "MO", "OH", "TX"] else "normal"
        x = row["size"] / 1000
        y = row["rate_pct"]
        ax.plot(x, y, "o", markersize=3, color=color, alpha=0.4)
        ax.annotate(state, (x, y), fontsize=6.5, ha="center", va="bottom",
                    color=color, fontweight=weight,
                    xytext=(0, 2), textcoords="offset points")

    # Quadrant lines
    ax.axhline(rate_med, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axvline(size_med / 1000, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

    # Quadrant labels
    ax.text(0.97, 0.97, "High turnover\nLarge workforce", transform=ax.transAxes,
            ha="right", va="top", fontsize=7, color=C_FCST, fontstyle="italic", alpha=0.8)
    ax.text(0.03, 0.97, "High turnover\nSmall workforce", transform=ax.transAxes,
            ha="left", va="top", fontsize=7, color=C_FCST, fontstyle="italic", alpha=0.8)
    ax.text(0.97, 0.03, "Low turnover\nLarge workforce", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7, color=C_OBS, fontstyle="italic", alpha=0.8)
    ax.text(0.03, 0.03, "Low turnover\nSmall workforce", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=7, color=C_OBS, fontstyle="italic", alpha=0.8)

    ax.set_xlabel("Nursing Home Workforce Size (employees)")
    ax.set_ylabel("Forecasted Monthly Separation Rate (%)")
    ax.set_title("Exhibit 4: State Workforce Risk — Forecasted Turnover Rate vs Workforce Size")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}K"))
    ax.grid(True, alpha=0.15)
    fig.text(0.5, 0.005,
             "Note: West Virginia (forecasted 18.6% separation rate, ~7,400 employees) is omitted for "
             "readability. Its forecast reflects a non-recurring June 2024 spike (33.9% that month, a\n"
             "facility-level event) that the seasonal method projects forward; WV's actual 2025 rate was ~7%.",
             ha="center", va="bottom", fontsize=6.5, color="#444444")
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(FIG_DIR / "exhibit4_state_quadrant.png")
    plt.close()
    print("  exhibit4_state_quadrant.png")


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
