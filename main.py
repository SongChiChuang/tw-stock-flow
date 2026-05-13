from modules.fetch_twse import fetch_twse_data
from modules.validation import validate_data
from modules.heatmap import generate_heatmap
from modules.accumulation import generate_accumulation
from modules.cleanup import cleanup_old_files
from modules.trading_calendar import is_trading_day

from utils.line_notify import send_line_message

import os


def main():

    if not is_trading_day():
        print("今日非交易日")
        return

    print("今日為交易日")

    # =========================
    # 抓資料
    # =========================

    df, date_str = fetch_twse_data()

    print(f"已儲存原始資料: data/{date_str}.csv")

    # =========================
    # 驗證
    # =========================

    validate_data(df)

    print("====================")
    print("Validation 完成")
    print("====================")

    # =========================
    # Heatmap
    # =========================

    print("📊 產生 foreign_buy_30")

    generate_heatmap(
        df=df,
        date_str=date_str,
        category="foreign",
        mode="buy"
    )

    print("📊 產生 foreign_sell_30")

    generate_heatmap(
        df=df,
        date_str=date_str,
        category="foreign",
        mode="sell"
    )

    print("📊 產生 trust_buy_30")

    generate_heatmap(
        df=df,
        date_str=date_str,
        category="trust",
        mode="buy"
    )

    print("📊 產生 trust_sell_30")

    generate_heatmap(
        df=df,
        date_str=date_str,
        category="trust",
        mode="sell"
    )

    # =========================
    # Accumulation
    # =========================

    print("📈 外資連續買超分析（>= 5 日）")

    generate_accumulation(
        min_days=5
    )

    # =========================
    # Cleanup
    # =========================

    print("🧹 開始資料清理")

    cleanup_old_files()

    print("✅ cleanup完成（封存 0 個檔案）")

    # =========================
    # LINE 推播
    # =========================

    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    dashboard_url = "https://songchichuang.github.io/tw-stock-flow/"

    message = f"""
TW Stock Flow 更新完成

資料日期：{date_str}

Dashboard：
{dashboard_url}
"""

    send_line_message(
        token=token,
        user_id=user_id,
        message=message
    )

    print("📨 LINE 通知已送出")

    print("🎉 main.py 執行完成")


if __name__ == "__main__":
    main()
