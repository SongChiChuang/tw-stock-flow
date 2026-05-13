import os
import pandas as pd


def generate_heatmap(
    df,
    date_str=None,
    category="foreign",
    mode=None
):

    if date_str is None:
        date_str = "unknown"

    if mode is not None:
        category = mode

    os.makedirs("reports/heatmap", exist_ok=True)

    df.columns = df.columns.str.strip()

    # 自動判斷欄位名稱
    possible_cols = [
        "買賣超股數",
        "買賣超",
        "外資買賣超股數",
        "投信買賣超股數"
    ]

    buy_col = None

    for col in possible_cols:
        if col in df.columns:
            buy_col = col
            break

    if buy_col is None:
        raise Exception(
            f"找不到買賣超欄位，目前欄位：{list(df.columns)}"
        )

    df[buy_col] = (
        df[buy_col]
        .astype(str)
        .str.replace(",", "")
        .astype(int)
    )

    buy_top30 = (
        df.sort_values(
            by=buy_col,
            ascending=False
        )
        .head(30)
    )

    sell_top30 = (
        df.sort_values(
            by=buy_col,
            ascending=True
        )
        .head(30)
    )

    buy_path = (
        f"reports/heatmap/"
        f"{date_str}_{category}_buy_30.csv"
    )

    sell_path = (
        f"reports/heatmap/"
        f"{date_str}_{category}_sell_30.csv"
    )

    buy_top30.to_csv(
        buy_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"📊 產生 {category}_buy_30")

    sell_top30.to_csv(
        sell_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"📊 產生 {category}_sell_30")
