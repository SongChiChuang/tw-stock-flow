import requests
import pandas as pd

from io import StringIO
from datetime import datetime

import time
import sys

# =========================================
# 時間設定 
# =========================================

START_HOUR = 16
END_HOUR = 21

EARLY_INTERVAL = 1800
LATE_INTERVAL = 600

# =========================================
# 抓取TWSE資料
# =========================================

def fetch_twse_data():

    today = datetime.now()

    today_str = today.strftime("%Y%m%d")

    url = (
        "https://www.twse.com.tw/rwd/zh/fund/T86"
        f"?date={today_str}&selectType=ALLBUT0999&response=csv"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    text = None

    # =====================================
    # 動態輪詢
    # =====================================

    while True:

        now = datetime.now()

        current_hour = now.hour

        # 超過21:00結束

        if current_hour >= END_HOUR:

            print("❌ 已超過21:00仍未取得資料")

            sys.exit(1)

        print(f"\n🔍 檢查時間: {now.strftime('%H:%M:%S')}")

        try:

            res = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            if res.status_code != 200:

                print(f"❌ HTTP錯誤: {res.status_code}")

            else:

                # cp950解碼

                text = res.content.decode(
                    "cp950",
                    errors="replace"
                )

                # 有資料

                if "證券代號" in text:

                    print("✅ 資料已更新")

                    break

                print("⏳ 資料尚未更新")

        except Exception as e:

            print(f"❌ 抓取失敗: {e}")

        # 16~18 每30分鐘

        if current_hour < 18:

            print("🕒 30分鐘後重試")

            time.sleep(EARLY_INTERVAL)

        # 18~21 每10分鐘

        else:

            print("🕒 10分鐘後重試")

            time.sleep(LATE_INTERVAL)

    # =====================================
    # 自動定位表頭
    # =====================================

    lines = text.splitlines()

    header_index = None

    for i, line in enumerate(lines):

        if (
            "證券代號" in line
            and
            "證券名稱" in line
        ):

            header_index = i

            break

    if header_index is None:

        print("❌ 找不到表頭")

        sys.exit(1)

    csv_text = "\n".join(lines[header_index:])

    # =====================================
    # CSV解析
    # =====================================

    try:

        df = pd.read_csv(
            StringIO(csv_text),
            encoding="cp950",
            thousands=",",
            dtype=str
        )

    except Exception as e:

        print(f"❌ CSV解析失敗: {e}")

        sys.exit(1)

    # =====================================
    # 移除空白列
    # =====================================

    df = df.dropna(how="all")

    print("✅ TWSE資料抓取成功")

    return df
