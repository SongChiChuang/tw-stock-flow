```python
# modules/accumulation.py
# =========================
# 外資累積買超分析（10日內 >= 8日買超）
# =========================

import pandas as pd
from pathlib import Path
from collections import defaultdict


def analyze_foreign_accumulation(
    lookback_days=10,
    min_buy_days=8,
    top_n=30
):

    print(
        f"📈 外資累積買超分析 "
        f"（最近 {lookback_days} 日內 >= {min_buy_days} 日買超）"
    )

    # =========================
    # 路徑
    # =========================

    data_dir = Path("data")
    output_dir = Path("reports/accumulation")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # =========================
    # 讀取CSV
    # =========================

    csv_files = sorted(
        data_dir.glob("20*.csv")
    )

    if len(csv_files) < lookback_days:

        print(
            f"❌ CSV檔案不足："
            f"目前 {len(csv_files)} 份"
        )

        return

    # 最近N日
    target_files = csv_files[-lookback_days:]

    print(
        "📦 使用資料:",
        [f.name for f in target_files]
    )

    # =========================
    # 統計容器
    # =========================

    stock_buy_days = defaultdict(int)
    stock_total_buy = defaultdict(float)
    stock_name_map = {}

    # =========================
    # 開始分析
    # =========================

    for file in target_files:

        try:

            # =========================
            # 讀CSV
            # =========================

            df = pd.read_csv(
                file,
                encoding="cp950"
            )

            print(f"✅ 已讀取: {file.name}")

            # =========================
            # 欄位清理
            # =========================

            df.columns = df.columns.str.strip()

            required_cols = [
                "證券代號",
                "證券名稱",
                "外陸資買賣超股數(不含外資自營商)"
            ]

            for col in required_cols:

                if col not in df.columns:

                    print(f"❌ 缺少欄位: {col}")
                    return

            # =========================
            # 保留必要欄位
            # =========================

            df = df[required_cols].copy()

            # =========================
            # 欄位改名
            # =========================

            df.columns = [
                "證券代號",
                "證券名稱",
                "買超張數"
            ]

            # =========================
            # 數值轉換
            # =========================

            df["買超張數"] = (
                df["買超張數"]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            df["買超張數"] = pd.to_numeric(
                df["買超張數"],
                errors="coerce"
            ).fillna(0)

            # =========================
            # 只保留買超
            # =========================

            df = df[
                df["買超張數"] > 0
            ]

            # =========================
            # 統計
            # =========================

            for _, row in df.iterrows():

                stock_id = str(row["證券代號"]).strip()

                stock_name = str(row["證券名稱"]).strip()

                buy_amount = float(row["買超張數"])

                # 買超天數 +1
                stock_buy_days[stock_id] += 1

                # 累積買超
                stock_total_buy[stock_id] += buy_amount

                # 股票名稱
                stock_name_map[stock_id] = stock_name

        except Exception as e:

            print(f"❌ 讀取失敗 {file.name}: {e}")

            return

    # =========================
    # 篩選 >= min_buy_days
    # =========================

    result = []

    for stock_id in stock_buy_days:

        buy_days = stock_buy_days[stock_id]

        if buy_days >= min_buy_days:

            result.append({

                "證券代號": stock_id,

                "證券名稱":
                    stock_name_map.get(stock_id, ""),

                "買超天數": buy_days,

                "累積買超張數":
                    int(stock_total_buy[stock_id])

            })

    # =========================
    # 無結果
    # =========================

    if len(result) == 0:

        print("⚠️ 無符合條件股票")

        return

    # =========================
    # DataFrame
    # =========================

    result_df = pd.DataFrame(result)

    # =========================
    # 排序
    # =========================

    result_df = result_df.sort_values(
        by="累積買超張數",
        ascending=False
    )

    # =========================
    # TOP N
    # =========================

    result_df = result_df.head(top_n)

    # =========================
    # 排名
    # =========================

    result_df.insert(
        0,
        "排名",
        range(1, len(result_df) + 1)
    )

    # =========================
    # 輸出CSV
    # =========================

    latest_date = target_files[-1].stem

    output_file = (
        output_dir /
        f"{latest_date}_foreign_accumulation.csv"
    )

    result_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    # =========================
    # 完成
    # =========================

    print(f"✅ 已輸出: {output_file}")

    print(result_df.head())
```
