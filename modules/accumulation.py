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

    # =====================================
    # data資料夾
    # =====================================

    data_folder = "data"

    # =====================================
    # 找csv
    # =====================================

    csv_files = [

        f for f in os.listdir(data_folder)

        if f.endswith(".csv")
    ]

    # =====================================
    # 排序
    # =====================================

    csv_files = sorted(csv_files)

    # =====================================
    # 取最近N日
    # =====================================

    recent_files = csv_files[-days:]

    print(f"📅 使用資料: {recent_files}")

    # =====================================
    # 合併資料
    # =====================================

    all_data = []

    for file in recent_files:

        filepath = (
            f"{data_folder}/{file}"
        )

        try:

            df = pd.read_csv(filepath)

            # 統一股票過濾

            df = filter_stocks(df)

            # 加日期欄位

            df["資料日期"] = (
                file.replace(".csv", "")
            )

            all_data.append(df)

            print(f"✅ 已讀取: {file}")

        except Exception as e:

            print(f"❌ 讀取失敗: {file}")

            print(e)

    # =====================================
    # 合併 dataframe
    # =====================================

    combined_df = pd.concat(
        all_data,
        ignore_index=True
    )

    print(
        f"✅ 合併完成 "
        f"(總筆數: {len(combined_df)})"
    )

    return combined_df
