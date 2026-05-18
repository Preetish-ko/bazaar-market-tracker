import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import os
from fetch_bazaar import fetch_bazaar, clean_data

os.makedirs("charts", exist_ok=True)

# Dark Skyblock theme
plt.rcParams.update({
    "figure.facecolor": "#0D0F14",
    "axes.facecolor":   "#13161E",
    "axes.edgecolor":   "#2A2D38",
    "text.color":       "#E8E8E0",
    "axes.labelcolor":  "#7A7D8A",
    "xtick.color":      "#7A7D8A",
    "ytick.color":      "#7A7D8A",
    "grid.color":       "#1A1E29",
    "grid.linestyle":   "--",
    "font.family":      "monospace",
})

def chart_top_margins(df):
    top = df.nlargest(20, "margin")
    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(top["name"], top["margin"],
                   color="#F5C842", alpha=0.85)
    ax.set_xlabel("Margin (coins per unit)")
    ax.set_title("Top 20 Bazaar Flip Margins", fontsize=14, color="#fff")
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig("charts/top_margins.png", dpi=150)
    plt.close()
    print("Saved charts/top_margins.png")

def chart_volume_vs_margin(df):
    fig, ax = plt.subplots(figsize=(11, 7))

    scatter = ax.scatter(
        df["weekly_buy_vol"], df["margin"],
        c=df["margin_pct"], cmap="YlOrRd",
        alpha=0.7, s=40
    )
    plt.colorbar(scatter, label="Margin %")

    # Label top 5 by margin
    for _, row in df.nlargest(5, "margin").iterrows():
        ax.annotate(row["name"],
                    (row["weekly_buy_vol"], row["margin"]),
                    fontsize=8, color="#F5C842",
                    xytext=(6, 4), textcoords="offset points")

    ax.set_xlabel("Weekly Buy Volume")
    ax.set_ylabel("Margin (coins)")
    ax.set_title("Volume vs Margin — Flip Opportunities",
                fontsize=14, color="#fff")
    ax.set_xscale("log")
    fig.tight_layout()
    fig.savefig("charts/volume_vs_margin.png", dpi=150)
    plt.close()

def chart_price_distribution(df):
    fig, ax = plt.subplots(figsize=(11, 6))
    # Log-scale the prices for a readable histogram
    ax.hist(df["buy_price"], bins=60,
            color="#4EA8FF", alpha=0.8, log=True)
    ax.set_xscale("log")
    ax.set_xlabel("Buy Price (coins, log scale)")
    ax.set_ylabel("Number of items")
    ax.set_title("Bazaar Price Distribution", fontsize=14, color="#fff")
    fig.tight_layout()
    fig.savefig("charts/price_distribution.png", dpi=150)
    plt.close()

if __name__ == "__main__":
    print("Fetching Bazaar data...")
    df = clean_data(fetch_bazaar())
    print(f"Analysing {len(df)} items...")

    chart_top_margins(df)
    chart_volume_vs_margin(df)
    chart_price_distribution(df)
    print("All charts saved to charts/")