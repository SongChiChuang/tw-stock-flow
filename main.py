# main.py

print("🚀 main.py 啟動")

# =========================
# Import Modules
# =========================

print("📦 import fetch_twse")
from modules.fetch_twse import fetch_twse_data

print("📦 import validation")
from modules.validation import run_validation

print("📦 import accumulation")
from modules.accumulation import analyze_foreign_accumulation

print("📦 import cleanup")
from modules.cleanup import cleanup_old_files

print("📦 import pandas")
import pandas as pd

print("📦 import os")
import os

print("✅ 所有 import 完成")


# =========================
# 外資 TOP30
# =========================

def generate_foreign_top30(csv_path):

    print("📊 產生外資 TOP30")

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

        target_col = "外陸資買賣超股數(不含外資自營商)"

        if target_col not in df.columns:

            print("❌ 缺少外資買賣超欄位")

            return

        # =========================
        # 數值轉換
        # =========================

        df[target_col] = (
            df[target_col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df[target_col] = pd.to_numeric(
            df[target_col],
            errors="coerce"
        ).fillna(0)

        # =========================
        # 買超 TOP30
        # =========================

        buy_df = df.sort_values(
            by=target_col,
            ascending=False
        ).head(30)

        # =========================
        # 賣超 TOP30
        # =========================

        sell_df = df.sort_values(
            by=target_col,
            ascending=True
        ).head(30)

        # =========================
        # 建立資料夾
        # =========================

        os.makedirs(
            "reports/foreign",
            exist_ok=True
        )

        # =========================
        # 日期
        # =========================

        file_date = os.path.basename(
            csv_path
        ).replace(".csv", "")

        # =========================
        # 輸出
        # =========================

        buy_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_buy_top30.csv"
        )

        sell_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_sell_top30.csv"
        )

        buy_df.to_csv(
            buy_path,
            index=False,
            encoding="utf-8-sig"
        )

        sell_df.to_csv(
            sell_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"✅ 已輸出: {buy_path}")
        print(f"✅ 已輸出: {sell_path}")

    except Exception as e:

        print("❌ 外資TOP30失敗")

        print(e)


# =========================
# 投信 TOP30
# =========================

def generate_investment_top30(csv_path):

    print("📊 產生投信 TOP30")

    try:

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        target_col = "投信買賣超股數"

        if target_col not in df.columns:

            print("❌ 缺少投信買賣超欄位")

            return

        # =========================
        # 數值轉換
        # =========================

        df[target_col] = (
            df[target_col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df[target_col] = pd.to_numeric(
            df[target_col],
            errors="coerce"
        ).fillna(0)

        # =========================
        # 買超 TOP30
        # =========================

        buy_df = df.sort_values(
            by=target_col,
            ascending=False
        ).head(30)

        # =========================
        # 賣超 TOP30
        # =========================

        sell_df = df.sort_values(
            by=target_col,
            ascending=True
        ).head(30)

        # =========================
        # 建立資料夾
        # =========================

        os.makedirs(
            "reports/investment",
            exist_ok=True
        )

        # =========================
        # 日期
        # =========================

        file_date = os.path.basename(
            csv_path
        ).replace(".csv", "")

        # =========================
        # 輸出
        # =========================

        buy_path = (
            f"reports/investment/"
            f"{file_date}_investment_buy_top30.csv"
        )

        sell_path = (
            f"reports/investment/"
            f"{file_date}_investment_sell_top30.csv"
        )

        buy_df.to_csv(
            buy_path,
            index=False,
            encoding="utf-8-sig"
        )

        sell_df.to_csv(
            sell_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"✅ 已輸出: {buy_path}")
        print(f"✅ 已輸出: {sell_path}")

    except Exception as e:

        print("❌ 投信TOP30失敗")

        print(e)


# =========================
# Main
# =========================

def main():

    print("🚀 開始執行 main()")

    # =========================
    # 抓取資料
    # =========================

    csv_path = fetch_twse_data()

    if csv_path is None:

        print("❌ 今日無資料")

        return

    # =========================
    # 驗證
    # =========================

    print("📥 開始驗證資料")

    validation_result = run_validation(
        csv_path
    )

    if validation_result is False:

        print("❌ validation失敗")

        return

    # =========================
    # TOP30
    # =========================

    generate_foreign_top30(csv_path)

    generate_investment_top30(csv_path)

    # =========================
    # 外資累積分析
    # =========================

    analyze_foreign_accumulation(
        lookback_days=10,
        min_buy_days=8
    )

    # =========================
    # 清理舊資料
    # =========================

    cleanup_old_files(days=20)

    print("🎉 main.py 執行完成")


# =========================
# Entry
# =========================

if __name__ == "__main__":

    main()
