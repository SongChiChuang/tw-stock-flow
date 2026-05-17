# modules/accumulation.py
# =========================
# 外資連續買超分析（TOP30）
# =========================

import pandas as pd
from pathlib import Path


def analyze_foreign_accumulation(days=3):
    print(f"📈 外資連續買超分析（>= {days} 日）")

    data_dir = Path("data")
    output_dir = Path("reports/accumulation")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(data_dir.glob("*.csv"))

    if len(csv_files) < days:
        print("❌ CSV檔案不足")
        return

    target_files = csv_files[-days:]

    print("📦 使用資料:", [f.name for f in target_files])

    all_data = []

    for file in target_files:
        try:
            df = pd.read_csv(file, encoding="cp950")

            print(f"✅ 已讀取: {file.name}")

            # 修正欄位名稱空白
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

            # 保留必要欄位
            df = df[required_cols].copy()

            # 欄位改名
            df.columns = [
                "證券代號",
                "證券名稱",
                "買超張數"
            ]

            # 數值轉換
            df["買超張數"] = (
                df["買超張數"]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            df["買超張數"] = pd.to_numeric(
                df["買超張數"],
                errors="coerce"
            ).fillna(0)

            # 僅保留買超
            df = df[df["買超張數"] > 0]

            all_data.append(df)

        except Exception as e:
            print(f"❌ 讀取失敗 {file.name}: {e}")
            return

    # =========================
    # 找連續買超
    # =========================

    stock_sets = [
        set(df["證券代號"])
        for df in all_data
    ]

    common_stocks = set.intersection(*stock_sets)

    if not common_stocks:
        print("⚠️ 無連續買超股票")
        return

    result = []

    for stock_id in common_stocks:

        total_buy = 0
        stock_name = ""

        for df in all_data:
            row = df[df["證券代號"] == stock_id]

            if not row.empty:
                total_buy += row.iloc[0]["買超張數"]
                stock_name = row.iloc[0]["證券名稱"]

        result.append({
            "證券代號": stock_id,
            "證券名稱": stock_name,
            "買超張數": int(total_buy)
        })

    result_df = pd.DataFrame(result)

    result_df = result_df.sort_values(
        by="買超張數",
        ascending=False
    )

    # TOP30
    result_df = result_df.head(30)

    # 排名
    result_df.insert(0, "排名", range(1, len(result_df) + 1))

    # 輸出
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

    print(f"✅ 已輸出: {output_file}")
    print(result_df.head())
