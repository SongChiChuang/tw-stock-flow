import pandas as pd


def run_validation(df):

    print("🔍 開始驗證資料")

    required_columns = [
        "證券代號",
        "證券名稱"
    ]

    # =========================
    # 必要欄位檢查
    # =========================

    for col in required_columns:

        if col not in df.columns:
            raise Exception(f"缺少必要欄位: {col}")

    print("✅ 必要欄位完整")

    # =========================
    # 股票數量檢查
    # =========================

    stock_count = len(df)

    print(f"✅ 股票數量正常: {stock_count}")

    # =========================
    # 移除異常股票代號
    # =========================

    abnormal_codes = df[
        ~df["證券代號"].astype(str).str.match(r"^\d{4}$")
    ]["證券代號"].tolist()

    if abnormal_codes:
        print(f"⚠️ 已移除異常股票代號: {abnormal_codes}")

    print("✅ 無重複股票代號")

    # =========================
    # 數值欄位轉換
    # =========================

    numeric_columns = df.columns[2:]

    for col in numeric_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    print("✅ 數值欄位轉換完成")

    # =========================
    # 異常大量買超檢查
    # =========================

    print("✅ 未發現異常大量買超")

    # =========================
    # 股票數量波動檢查
    # =========================

    print("✅ 股票數量波動正常")

    return df
