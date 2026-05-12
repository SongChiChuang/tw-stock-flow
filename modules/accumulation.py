import os
import pandas as pd

from utils.stock_filter import (
    filter_stocks
)

# =========================================
# 讀取最近 N 日資料
# =========================================

def load_recent_data(days=10):

    print(f"\n📂 讀取最近 {days} 日資料")

    data_folder = "data"

    csv_files = [

        f for f in os.listdir(data_folder)

        if f.endswith(".csv")
    ]

    csv_files = sorted(csv_files)

    recent_files = csv_files[-days:]

    print(f"📅 使用資料: {recent_files}")

    all_data = []

    for file in recent_files:

        filepath = (
            f"{data_folder}/{file}"
        )

        try:

            df = pd.read_csv(filepath)

            # 股票過濾

            df = filter_stocks(df)

            # 日期欄位

            df["資料日期"] = (
                file.replace(".csv", "")
            )

            all_data.append(df)

            print(f"✅ 已讀取: {file}")

        except Exception as e:

            print(f"❌ 讀取失敗: {file}")

            print(e)

    combined_df = pd.concat(
        all_data,
        ignore_index=True
    )

    print(
        f"✅ 合併完成 "
        f"(總筆數: {len(combined_df)})"
    )

    return combined_df

# =========================================
# 外資持續買超
# =========================================

def generate_foreign_accumulation(
    recent_df,
    today_str,
    min_buy_days=8
):

    print(
        f"\n📊 外資連續買超分析 "
        f"(>= {min_buy_days} 日)"
    )

    # =====================================
    # 外資買超
    # =====================================

    foreign_col = (
        "外陸資買賣超股數(不含外資自營商)"
    )

    buy_df = recent_df[
        recent_df[foreign_col] > 0
    ]

    # =====================================
    # groupby
    # =====================================

    grouped = (

        buy_df.groupby(

            [
                "證券代號",
                "證券名稱"
            ]

        )

        ["資料日期"]

        .nunique()

        .reset_index()

    )

    # =====================================
    # rename
    # =====================================

    grouped.columns = [

        "證券代號",
        "證券名稱",
        "買超天數"

    ]

    # =====================================
    # 條件
    # =====================================

    result_df = grouped[

        grouped["買超天數"]
        >= min_buy_days

    ]

    # =====================================
    # 排序
    # =====================================

    result_df = result_df.sort_values(

        by="買超天數",
        ascending=False

    )

    # =====================================
    # 建立資料夾
    # =====================================

    os.makedirs(
        "reports/accumulation",
        exist_ok=True
    )

    # =====================================
    # 輸出
    # =====================================

    filename = (

        f"reports/accumulation/"
        f"{today_str}_foreign_accumulation.csv"

    )

    result_df.to_csv(

        filename,

        index=False,

        encoding="utf-8-sig"

    )

    print(f"✅ 已輸出: {filename}")

    print(result_df.head())
