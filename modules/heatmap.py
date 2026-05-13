import os
import pandas as pd


def generate_heatmap(df, date_str=None):

    if date_str is None:
        date_str = "unknown"

    os.makedirs("reports/heatmap", exist_ok=True)

    df.columns = df.columns.str.strip()

    buy_col = "買賣超股數"

    df[buy_col] = (
        df[buy_col]
        .astype(str)
        .str.replace(",", "")
        .astype(int)
    )

    foreign_buy = (
        df.sort_values(by=buy_col, ascending=False)
        .head(30)
    )

    foreign_sell = (
        df.sort_values(by=buy_col, ascending=True)
        .head(30)
    )

    foreign_buy.to_csv(
        f"reports/heatmap/{date_str}_foreign_buy_30.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("📊 產生 foreign_buy_30")

    foreign_sell.to_csv(
        f"reports/heatmap/{date_str}_foreign_sell_30.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("📊 產生 foreign_sell_30")
