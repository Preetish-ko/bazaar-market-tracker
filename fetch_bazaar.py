import requests
import pandas as pd
from datetime import datetime

URL = "https://api.hypixel.net/skyblock/bazaar"

def fetch_bazaar():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("success"):
        raise ValueError("API returned success=false")

    rows = []
    for item_id, product in data["products"].items():
        qs = product.get("quick_status", {})
        buy  = qs.get("buyPrice", 0)
        sell = qs.get("sellPrice", 0)
        rows.append({
            "item_id":          item_id,
            "name":             item_id.replace("_", " ").title(),
            "buy_price":        round(buy, 2),
            "sell_price":       round(sell, 2),
            "margin":           round(buy - sell, 2),
            "margin_pct":       round((buy - sell) / buy * 100, 2) if buy > 0 else 0,
            "buy_volume":       qs.get("buyVolume", 0),
            "sell_volume":      qs.get("sellVolume", 0),
            "weekly_buy_vol":   qs.get("buyMovingWeek", 0),
            "weekly_sell_vol":  qs.get("sellMovingWeek", 0),
            "fetched_at":       datetime.utcnow().isoformat(),
        })

    return pd.DataFrame(rows)

def clean_data(df):
    # Remove items with zero or negative prices
    df = df[df["buy_price"] > 0]
    df = df[df["sell_price"] > 0]
    # Keep only items with meaningful weekly volume
    df = df[df["weekly_buy_vol"] > 1000]
    # Keep only positive margins
    df = df[df["margin"] > 0]
    return df.reset_index(drop=True)

if __name__ == "__main__":
    df = fetch_bazaar()
    print(df.head())
    print(f"Fetched {len(df)} items")