# main.py

from modules.fetch_twse import fetch_twse_data
from modules.validation import run_validation
from modules.cleanup import cleanup_old_files
from modules.accumulation import analyze_foreign_accumulation

import pandas as pd
from pathlib import Path


def main():

    print("📅 今日交易日")

    # =========================
    # 抓取資料
    # =========================

    csv_path = fetch_twse_data()

    if csv_path is None:
        print("❌ 今日無資料")
        return

    # =========================
    # 讀取CSV
    # =========================

    try:

        df = pd.read_csv(
            csv_path,
            encoding="cp950"
        )

        print("📥 開始驗證資料")

    except Exception as e:

        print(f"❌ CSV讀取失敗: {e}")
        return

    # =========================
    # 資料驗證
    # =========================

    try:

        run_validation(df)

    except Exception as e:

        print(f"❌ 驗證失敗: {e}")
        return

    # =========================
    # 外資累積分析
    # =========================

    try:

        analyze_foreign_accumulation(
            lookback_days=10,
            min_buy_days=8
        )

    except Exception as e:

        print(f"❌ 累積分析失敗: {e}")

    # =========================
    # 清理舊資料
    # =========================

    try:

        cleanup_old_files(days=20)

    except Exception as e:

        print(f"❌ cleanup失敗: {e}")

    print("🎉 main.py 執行完成")


if __name__ == "__main__":
    main()
