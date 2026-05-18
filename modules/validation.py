# modules/validation.py
# =========================
# 資料驗證模組
# =========================

import pandas as pd


def run_validation(df):

    print("🔎 開始驗證資料")

    # =========================
    # 欄位清理
    # =========================

    df.columns = df.columns.str.strip()

    print("📋 DataFrame 欄位:")
    print(df.columns.tolist())

    # =========================
    # 必要欄位
    # =========================

    required_cols = [
        "證券代號",
        "證券名稱",
        "外陸資買賣超股數(不含外資自營商)"
    ]

    for col in required_cols:

        if col not in df.columns:
            raise Exception(f"缺少必要欄位: {col}")

    print("✅ 必要欄位完整")

    # =========================
    # 股票代號格式修正
    # =========================

    df["證券代號"] = (
        df["證券代號"]
        .astype(str)
        .str.replace('="', '', regex=False)
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    # =========================
    # 排除 ETF / 權證 / 特殊商品
    # =========================

    exclude_prefix = (
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09"
    )

    before_count = len(df)

    df = df[
        ~df["證券代號"].str.startswith(exclude_prefix)
    ]

    after_count = len(df)

    print(f"🧹 已排除ETF/特殊商品: {before_count - after_count}")

    # =========================
    # 股票數量驗證
    # =========================

    stock_count = len(df)

    print(f"📊 股票數量: {stock_count}")

    # 台股上市非ETF正常約700~1000
    if stock_count < 500:
        raise Exception("股票數量過少")

    print("✅ 股票數量正常")

    # =========================
    # 數值欄位清理
    # =========================

    numeric_cols = [
        "外陸資買賣超股數(不含外資自營商)"
    ]

    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    print("✅ 數值欄位轉換完成")

    # =========================
    # 異常值檢查
    # =========================

    abnormal = df[
        df["外陸資買賣超股數(不含外資自營商)"].abs() > 500000000
    ]

    if not abnormal.empty:

        print("⚠️ 發現異常股票代號:")
        print(abnormal["證券代號"].tolist())

    else:
        print("✅ 未發現異常大量買超")

    # =========================
    # 波動檢查
    # =========================

    if (
        df["外陸資買賣超股數(不含外資自營商)"]
        .abs()
        .sum()
        <= 0
    ):
        raise Exception("買賣超資料異常")

    print("✅ 股票數量波動正常")

    print("====================")
    print("Validation 完成")
    print("====================")

    return df
