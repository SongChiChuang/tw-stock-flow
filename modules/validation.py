# modules/validation.py

import pandas as pd


def run_validation(csv_path):

    print("🔎 開始驗證資料")

    try:

        # =========================
        # UTF-8-SIG
        # =========================

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        print("📋 DataFrame 欄位:")
        print(df.columns.tolist())

        if len(df) < 100:

            print("❌ 股票數量過少")

            return False

        print(f"📊 股票數量: {len(df)}")

        print("✅ 驗證成功")

        return True

    except Exception as e:

        print(f"❌ CSV讀取失敗: {e}")

        return False
