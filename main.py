import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os
import time

# ========= 日期 =========
today = datetime.today()
today_str = today.strftime("%Y%m%d")

url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={today_str}&selectType=ALLBUT0999&response=csv"

print(f"🚀 開始監控資料：{today_str}")

# ========= 監控邏輯 =========
while True:

    now = datetime.now()
    hour = now.hour

    print(f"🕒 現在時間：{now.strftime('%H:%M:%S')}")
    print("🔍 嘗試抓取資料...")

    try:
        res = requests.get(url, timeout=30)
        text = res.text
    except Exception as e:
        print("❌ 請求失敗：", e)
        text = ""

    # ========= 成功取得 =========
    if "證券代號" in text:

        print("✅ 資料已取得")

        # ========= 找表頭 =========
        lines = text.split("\n")

        start = 0
        for i, line in enumerate(lines):
            if "證券代號" in line:
                start = i
                break

        clean_data = "\n".join(lines[start:])

        df = pd.read_csv(StringIO(clean_data))

        # ========= 建資料夾 =========
        os.makedirs("data", exist_ok=True)

        # ========= 存檔 =========
        filename = f"data/{today_str}.csv"

        df.to_csv(filename, index=False)

        print(f"✅ 已儲存：{filename}")

        print(df.head())

        break

    # ========= 超過21:00停止 =========
    if hour >= 21:
        print("❌ 已超過21:00，今日仍無資料")
        break

    # ========= 分段等待 =========
    if hour < 18:
        wait_time = 1800   # 30分鐘
        print("⏳ 16~18點區間，30分鐘後再試")
    else:
        wait_time = 600    # 10分鐘
        print("⏳ 18~21點區間，10分鐘後再試")

    time.sleep(wait_time)

print("🏁 程式結束")
