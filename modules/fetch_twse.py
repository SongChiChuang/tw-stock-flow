# modules/fetch_twse.py
# =========================
# 抓取 TWSE T86 資料
# =========================

import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime
import time


def fetch_twse_data():

    today = datetime.now().strftime("%Y%m%d")

    print("📅 今日交易日")
    print("📡 資料更新")

    url = (
        "https://www.twse.com.tw/rwd/zh/fund/T86"
        f"?date={today}"
        "&selectType=ALLBUT0999"
        "&response=csv"
    )

    for attempt in range(3):

        try:

            print(f"🌐 第 {attempt + 1} 次抓取")

            response = requests.get(
                url,
                timeout=30
            )

            if response.status_code != 200:
                print(f"❌ HTTP錯誤: {response.status_code}")
                time.sleep(3)
                continue

            # =========================
            # TWSE 使用 BIG5(cp950)
            # =========================
            response.encoding = "cp950"

            raw_text = response.text

            print("========== TWSE RAW ==========")
            print(raw_text[:3000])
            print("========== END RAW ==========")

            if "證券代號" not in raw_text:
                print("❌ 清洗後無有效資料")
                time.sleep(3)
                continue

            # =========================
            # 清洗資料
            # =========================

            lines = raw_text.splitlines()

            cleaned_lines = []

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("="):
                    continue

                if "證券代號" in line:
                    cleaned_lines.append(line)
                    continue

                if line.startswith('"='):
                    cleaned_lines.append(line)

            if len(cleaned_lines) <= 1:
                print("❌ 今日無資料")
                time.sleep(3)
                continue

            csv_text = "\n".join(cleaned_lines)

            df = pd.read_csv(StringIO(csv_text))

            print("✅ DataFrame建立成功")

            # =========================
            # 儲存
            # =========================

            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)

            output_file = data_dir / f"{today}.csv"

            df.to_csv(
                output_file,
                index=False,
                encoding="cp950"
            )

            print(f"✅ 已儲存: {output_file}")

            return output_file

        except Exception as e:

            print(f"❌ 抓取失敗: {e}")

            time.sleep(3)

    print("❌ 三次抓取全部失敗")
    return None
