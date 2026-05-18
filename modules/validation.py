# modules/validation.py
# =========================
# CSV 驗證模組
# =========================

import pandas as pd
import traceback

from utils.stock_filter import is_stock


def run_validation(csv_path):

    print("🔎 開始驗證資料")

    try:

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        print("📋 DataFrame 欄位:")
        print(df.columns.tolist())

        # =========================
        # 清理欄位空白
        # =========================
        df.columns = df.columns.str.strip()

        # =========================
        # 必要欄位
        # =========================
        required_columns = [
            "證券代號",
            "證券名稱",
        ]

        for col in required_columns:

            if col not in df.columns:
                print(f"❌ 缺少欄位: {col}")
                return False

        print("✅ 必要欄位完整")

        # =========================
        # 排除 ETF / 特殊商品
        # =========================
        before_count = len(df)

        df = df[
            df.apply(
                lambda row: is_stock(
                    row["證券代號"],
                    row["證券名稱"]
                ),
                axis=1
            )
        ]

        removed_count = before_count - len(df)

        print(f"🧹 已排除無效代號: {removed_count}")

        # =========================
        # 股票數量
        # =========================
        stock_count = len(df)

        print(f"📊 股票數量: {stock_count}")

        if stock_count < 500:
            print("❌ 驗證失敗：股票數量過少")
            return False

        print("✅ 驗證成功")

        return True

    except Exception:

        print("❌ 完整錯誤如下：")

        traceback.print_exc()

        return False
