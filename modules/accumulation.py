# modules/accumulation.py
# =========================
# 外資近10日累積買超分析
# 條件：
# 1. 全上市股票
# 2. 最近10個交易日中 >= 8日買超
# 3. 依累積買超排序 TOP30
# =========================

import pandas as pd
from pathlib import Path


def analyze_foreign_accumulation(
    lookback_days=10,
    min_buy_days=8
):

    print("📈 外資近10日累積買超分析")

    data_dir = Path("data")
    output_dir = Path("reports/accumulation")

    output_dir.mkdir(parents=True, exist_ok=True)

    # =========================
    # 取得最近 N 日資料
    # =========================

    csv_files = sorted(data_dir.glob("*.csv"))

    if len(csv_files) < lookback_days:
        print("❌ CSV檔案不足")
        return

    target_files = csv_files[-lookback_days:]

    print("📦 使用資料：")
    for f in target_files:
        print("   ", f.name)

    # =========================
    # 合併所有日期資料
    # =========================

    all_rows = []

    for file in target_files:

        try:

            df = pd.read_csv(
                file,
                encoding="cp950"
            )

            print(f"✅ 已讀取: {file.name}")

            # 清理欄位
            df.columns = df.columns.str.strip()

            required_cols = [
                "證券代號",
                "證券名稱",
                "外陸資買賣超股數(不含外資自營商)"
            ]

            for col in required_cols:

                if col not in df.columns:
                    raise Exception(f"缺少欄位: {col}")

            df = df[required_cols].copy()

            # 改名
            df.columns = [
                "證券代號",
                "證券名稱",
                "買超張數"
            ]

            # 數值清理
            df["買超張數"] = (
                df["買超張數"]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            df["買超張數"] = pd.to_numeric(
                df["買超張數"],
                errors="coerce"
            ).fillna(0)

            # 加入日期
            df["日期"] = file.stem

            all_rows.append(df)

        except Exception as e:

            print(f"❌ 讀取失敗 {file.name}: {e}")
            return

    # =========================
    # 合併資料
    # =========================

    combined_df = pd.concat(
        all_rows,
        ignore_index=True
    )

    # =========================
    # 僅保留買超
    # =========================

    combined_df = combined_df[
        combined_df["買超張數"] > 0
    ]

    # =========================
    # 統計：
    # 1. 買超天數
    # 2. 累積買超
    # =========================

    grouped = combined_df.groupby(
        ["證券代號", "證券名稱"]
    ).agg(
        買超天數=("日期", "nunique"),
        累積買超=("買超張數", "sum")
    ).reset_index()

    # =========================
    # 篩選 >= 8日買超
    # =========================

    grouped = grouped[
        grouped["買超天數"] >= min_buy_days
    ]

    if grouped.empty:

        print("⚠️ 無符合條件股票")
        return

    # =========================
    # 排序
    # =========================

    grouped = grouped.sort_values(
        by="累積買超",
        ascending=False
    )

    # TOP30
    grouped = grouped.head(30)

    # 排名
    grouped.insert(
        0,
        "排名",
        range(1, len(grouped) + 1)
    )

    # =========================
    # 輸出
    # =========================

    latest_date = target_files[-1].stem

    output_file = (
        output_dir /
        f"{latest_date}_foreign_accumulation.csv"
    )

    grouped.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✅ 已輸出: {output_file}")

    print(grouped.head(10))
