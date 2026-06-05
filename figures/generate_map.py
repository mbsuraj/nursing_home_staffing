"""
Generate Exhibit 2: choropleth map of state separation rates.
Uses Albers-style layout with AK and HI repositioned as floating insets
in the bottom-left, matching standard US thematic map convention.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

plt.rcParams.update({
    "font.size": 10,
    "font.family": "sans-serif",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

FIG_DIR = Path(__file__).parent
DATA_DIR = Path(__file__).parent.parent / "data"

# State abbreviation mapping
STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
}


def reposition(geom_series, scale, x_off, y_off, anchor):
    """Scale a geometry about an anchor point then translate."""
    from shapely.affinity import scale as sscale, translate as stranslate
    g = sscale(geom_series, xfact=scale, yfact=scale, origin=anchor)
    g = stranslate(g, xoff=x_off, yoff=y_off)
    return g


def main():
    us = gpd.read_file(FIG_DIR / "us-states.json")
    us["state"] = us["name"].map(STATE_ABBREV)

    # Turnover rates
    panel = pd.read_csv(DATA_DIR / "panel.csv", parse_dates=["month_end"])
    emp = panel[panel["worker_type"] == "Employee"]
    train = emp[emp["month_end"] <= "2025-03-01"]
    rates = train.groupby("state").apply(
        lambda g: g["separation_count"].sum() / g["active_count"].sum(), include_groups=False
    ).reset_index(name="rate")
    us = us.merge(rates, on="state", how="left")

    # Split into continental, AK, HI
    cont = us[~us["state"].isin(["AK", "HI", "PR", "GU"])].copy()
    ak = us[us["state"] == "AK"].copy()
    hi = us[us["state"] == "HI"].copy()

    # Reposition AK (shrink, move to bottom-left under CA/AZ)
    if not ak.empty:
        ak["geometry"] = ak["geometry"].apply(
            lambda g: reposition(g, 0.35, 33, -36, anchor=(-150, 62))
        )
    # Reposition HI (move to bottom-left, right of AK)
    if not hi.empty:
        hi["geometry"] = hi["geometry"].apply(
            lambda g: reposition(g, 1.0, 52, 6, anchor=(-157, 20))
        )

    combined = pd.concat([cont, ak, hi])

    fig, ax = plt.subplots(1, 1, figsize=(11, 6.5))
    cmap = LinearSegmentedColormap.from_list(
        "turnover", ["#f7fbff", "#9ecae1", "#4292c6", "#08519c", "#9b2335"], N=256
    )

    vmin, vmax = 0.04, 0.12
    combined.plot(
        column="rate", ax=ax, cmap=cmap, edgecolor="white", linewidth=0.4,
        vmin=vmin, vmax=vmax,
        legend=True,
        legend_kwds={
            "label": "Average Monthly Separation Rate",
            "orientation": "horizontal", "shrink": 0.5, "pad": 0.01, "aspect": 30,
        },
        missing_kwds={"color": "lightgray"},
    )

    # Format colorbar as percent
    cb = ax.get_figure().axes[-1]
    cb.set_xticklabels([f"{float(t.get_text().replace('−','-'))*100:.0f}%"
                        for t in cb.get_xticklabels()])

    ax.set_xlim(-128, -65)
    ax.set_ylim(20, 52)
    ax.axis("off")
    ax.set_title(
        "Exhibit 1: Average Monthly Employee Separation Rate by State, October 2022–March 2025",
        fontsize=11, pad=8,
    )

    # Label extreme states (continental only)
    for _, row in cont.iterrows():
        if row["state"] in ["MO", "OK", "OH", "TX", "KS", "NY"] and pd.notna(row["rate"]):
            c = row["geometry"].centroid
            ax.annotate(row["state"], xy=(c.x, c.y), ha="center", va="center",
                        fontsize=6, fontweight="bold",
                        color="white" if row["rate"] > 0.09 else "black")
    ax.annotate("AK", xy=(-117, 24), fontsize=6, fontweight="bold", ha="center")
    ax.annotate("HI", xy=(-104, 24), fontsize=6, fontweight="bold", ha="center")

    fig.savefig(FIG_DIR / "exhibit1_state_map.png")
    plt.close()
    print("Saved exhibit1_state_map.png (with AK and HI insets)")


if __name__ == "__main__":
    main()
