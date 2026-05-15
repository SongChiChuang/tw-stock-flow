import os
from datetime import datetime

from modules.fetch_twse import fetch_twse_data
from modules.validation import run_validation
from modules.heatmap import generate_heatmap
from modules.accumulation import generate_accumulation
from modules.cleanup import cleanup_old_files


def main():
    print("📅 今日交易日")

    # =========================
    # 抓取 TWSE 資料
    # =========================
    print("📥 資料已更新")

    df, date_str = fetch_twse_data()

    print("✅ TWSE資料抓取成功")

    # =========================
    # 儲存原始資料
    # =========================
    os.makedirs("data", exist_ok=True)

    csv_path = f"data/{date_str}.csv"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"📁 已儲存原始資料: {csv_path}")

    # =========================
    # 驗證資料
    # =========================
    print("🔍 開始驗證資料")

    run_validation(df)

    print("====================")
    print("Validation 完成")
    print("====================")

    # =========================
    # 產生 Heatmap
    # =========================
    print("📊 產生 heatmap")

    generate_heatmap()

    # =========================
    # 產生累積分析
    # =========================
    print("📈 產生 foreign_buy_30")

    generate_accumulation()

    # =========================
    # 清理舊檔案
    # =========================
    print("🧹 開始資料清理")

    cleanup_old_files()

    print("✅ cleanup完成")

    # =========================
    # 完成
    # =========================
    print("🎉 main.py 執行完成")


if __name__ == "__main__":
    main()
