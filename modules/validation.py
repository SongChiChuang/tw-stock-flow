# modules/validation.py

import pandas as pd


def run_validation(csv_path):

    print("🔎 開始驗證資料")

    try:

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        # =========================
        # 欄位清理
        # =========================

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        print("📋 DataFrame 欄位:")
        print(df.columns.tolist())

        # =========================
        # 必要欄位
        # =========================

        required_columns = [
            "證券代號",
            "證券名稱"
        ]

        for col in required_columns:

            if col not in df.columns:
                print(f"❌ 缺少欄位: {col}")
                return False

        # =========================
        # 股票數量
        # =========================

        stock_count = len(df)

        print(f"📊 股票數量: {stock_count}")

        if stock_count < 100:

            print("❌ 股票數量過少")

            return False

        print("✅ 驗證成功")

        return True

    except Exception as e:

        print(f"❌ CSV讀取失敗: {e}")

        return False
