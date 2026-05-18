# modules/validation.py
# =========================
# 資料驗證模組
# =========================

import pandas as pd


def run_validation(df):

    print("🔎 開始驗證資料")

    # =========================
    # 欄位名稱清理
    # =========================

    df.columns = df.columns.str.strip()

    print("📋 DataFrame 欄位:")
    print(df.columns.tolist())

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
    # 股票代號清洗
    # =========================

    df["證券代號"] = (
        df["證券代號"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.replace('=', '', regex=False)
        .str.strip()
    )

    df["證券名稱"] = (
        df["證券名稱"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    # =========================
    # 排除 ETF / 特殊商品
    # =========================

    etf_keywords = [
        "ETF",
        "特別股",
        "槓桿",
        "反向",
        "期貨",
        "正2",
        "反1",
        "反向1",
        "台灣50",
        "高股息",
        "科技債",
        "金融債",
        "公司債",
        "美債",
        "國泰",
        "元大",
        "富邦",
        "群益",
        "復華",
        "永豐",
        "中信",
        "兆豐"
    ]

    before_count = len(df)

    df = df[
        ~df["證券名稱"].str.contains(
            "|".join(etf_keywords),
            na=False
        )
    ]

    after_count = len(df)

    print(f"🧹 已排除ETF/特殊商品: {before_count - after_count}")

    # =========================
    # 僅保留上市股票
    # =========================

    df = df[
        df["證券代號"].str.match(r"^[0-9]{4}$", na=False)
    ]

    # =========================
    # 股票數量驗證
    # =========================

    stock_count = len(df)

    print(f"📊 股票數量: {stock_count}")

    if stock_count < 100:
        raise Exception("股票數量過少")

    print("✅ 股票數量正常")

    # =========================
    # 數值欄位轉換
    # =========================

    numeric_cols = [
        "外陸資買賣超股數(不含外資自營商)"
    ]

    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace('"', '', regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    print("✅ 數值欄位轉換完成")

    return df
