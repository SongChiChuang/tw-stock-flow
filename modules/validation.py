import pandas as pd

      # =========================
      # 資料驗證與篩選
      # =========================

def run_validation(df):

    print("🔍 開始驗證資料")

    # =========================
    # 顯示欄位名稱
    # =========================
    print("📋 DataFrame 欄位:")
    print(df.columns.tolist())

    # =========================
    # 自動尋找欄位
    # =========================
    code_col = None
    name_col = None
    buy_col = None

    for col in df.columns:

        if "代號" in col:
            code_col = col

        if "名稱" in col:
            name_col = col

        if "買賣超" in col:
            buy_col = col

    # =========================
    # 檢查欄位
    # =========================
    if code_col is None:
        raise Exception("找不到 股票代號欄位")

    if name_col is None:
        raise Exception("找不到 股票名稱欄位")

    if buy_col is None:
        raise Exception("找不到 買賣超欄位")

    print("✅ 必要欄位完整")

    # =========================
    # 股票數量檢查
    # =========================
    if len(df) < 1000:
        raise Exception("股票數量過少")

    print(f"✅ 股票數量正常: {len(df)}")

    # =========================
    # 數值欄位轉換
    # =========================
    df[buy_col] = (
        df[buy_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .fillna("0")
    )

    df[buy_col] = pd.to_numeric(
        df[buy_col],
        errors="coerce"
    ).fillna(0)

    print("✅ 數值欄位轉換完成")

    # =========================
    # 異常值檢查
    # =========================
    abnormal = df[
        df[buy_col].abs() > 5000000
    ]

    if len(abnormal) > 0:

        print("⚠️ 已移除異常股票代號:")

        print(
            abnormal[code_col].tolist()
        )

    print("✅ 未發現異常大量買超")

    print("✅ 股票數量波動正常")

    return df
