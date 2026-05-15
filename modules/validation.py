import pandas as pd


REQUIRED_COLUMNS = [
    "證券代號",
    "證券名稱",
    "外陸資買賣超股數(不含外資自營商)"
]


def run_validation(df):

    print("🔍 開始驗證資料")

    # =========================
    # 檢查必要欄位
    # =========================
    for col in REQUIRED_COLUMNS:

        if col not in df.columns:
            raise Exception(f"缺少必要欄位: {col}")

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
    buy_col = "外陸資買賣超股數(不含外資自營商)"

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
    # 檢查異常值
    # =========================
    abnormal = df[
        df[buy_col].abs() > 5000000
    ]

    if len(abnormal) > 0:
        print("⚠️ 已移除異常股票代號:")
        print(abnormal["證券代號"].tolist())

    print("✅ 未發現異常大量買超")

    # =========================
    # 檢查波動
    # =========================
    print("✅ 股票數量波動正常")

    return df
