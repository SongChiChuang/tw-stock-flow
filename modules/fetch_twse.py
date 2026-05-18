# modules/fetch_twse.py

import requests
import pandas as pd

from io import StringIO
from pathlib import Path
from datetime import datetime


def fetch_twse_data():

    print("📥 資料更新")

    today = datetime.now().strftime("%Y%m%d")

    url = (
        "https://www.twse.com.tw/rwd/zh/fund/T86"
        f"?date={today}"
        "&selectType=ALLBUT0999"
        "&response=csv"
    )

    try:

        response = requests.get(
            url,
            timeout=30
        )

        response.encoding = "utf-8"

        raw_text = response.text

        # =========================
        # 基本防呆
        # =========================

        if not raw_text.strip():

            print("❌ TWSE回傳空資料")
            return None

        if "很抱歉" in raw_text:

            print("❌ 今日無交易資料")
            return None

        if "<html" in raw_text.lower():

            print("❌ TWSE回傳HTML")
            return None

        # =========================
        # 清洗CSV
        # =========================

        lines = raw_text.split("\n")

        cleaned_lines = []

        start_collect = False

        for line in lines:

            line = line.strip()

            # 找表頭
            if "證券代號" in line:

                start_collect = True

            if not start_collect:
                continue

            # 跳過空行
            if not line:
                continue

            # 跳過說明文字
            if "說明" in line:
                continue

            if "備註" in line:
                continue

            # 只保留有逗號的行
            if "," not in line:
                continue

            cleaned_lines.append(line)

        if len(cleaned_lines) <= 1:

            print("❌ 清洗後無有效資料")
            return None

        csv_text = "\n".join(cleaned_lines)

        # =========================
        # 讀取CSV
        # =========================

        df = pd.read_csv(
            StringIO(csv_text)
        )

        if df.empty:

            print("❌ DataFrame為空")
            return None

        # =========================
        # 儲存
        # =========================

        output_dir = Path("data")

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_dir / f"{today}.csv"

        df.to_csv(
            output_file,
            index=False,
            encoding="cp950"
        )

        print("✅ TWSE資料抓取成功")
        print(f"✅ 已儲存: {output_file}")

        return output_file

    except Exception as e:

        print(f"❌ fetch_twse_data失敗: {e}")

        return None
