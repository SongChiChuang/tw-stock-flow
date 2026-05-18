# modules/fetch_twse.py

import time
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

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/136.0 Safari/537.36"
        )
    }

    # =========================
    # Retry 機制
    # =========================

    for attempt in range(3):

        try:

            print(f"🌐 第 {attempt + 1} 次抓取")

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            response.encoding = "utf-8"

            raw_text = response.text

            # =========================
            # Debug輸出
            # =========================

            print("========== TWSE RAW ==========")
            print(raw_text[:1000])
            print("========== END RAW ==========")

            # =========================
            # 基本防呆
            # =========================

            if not raw_text.strip():

                print("❌ TWSE回傳空資料")

                time.sleep(3)
                continue

            if "<html" in raw_text.lower():

                print("❌ TWSE回傳HTML")

                time.sleep(3)
                continue

            if "很抱歉" in raw_text:

                print("📴 今日無交易資料")
                return None

            # =========================
            # 清洗CSV
            # =========================

            lines = raw_text.split("\n")

            cleaned_lines = []

            start_collect = False

            for line in lines:

                line = line.strip()

                # 去除 BOM
                line = line.replace("\ufeff", "")

                # 找真正表頭
                if (
                    "證券代號" in line
                    and "證券名稱" in line
                ):
                    start_collect = True

                if not start_collect:
                    continue

                # 空行跳過
                if not line:
                    continue

                # 說明文字跳過
                if "說明" in line:
                    continue

                if "備註" in line:
                    continue

                # 非CSV跳過
                if "," not in line:
                    continue

                cleaned_lines.append(line)

            # =========================
            # 清洗結果檢查
            # =========================

            if len(cleaned_lines) <= 1:

                print("❌ 清洗後無有效資料")

                time.sleep(3)
                continue

            csv_text = "\n".join(cleaned_lines)

            print("========== CLEAN CSV ==========")
            print(csv_text[:1000])
            print("========== END CSV ==========")

            # =========================
            # 讀CSV
            # =========================

            df = pd.read_csv(
                StringIO(csv_text)
            )

            if df.empty:

                print("❌ DataFrame為空")

                time.sleep(3)
                continue

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

            time.sleep(3)

    # =========================
    # 最終失敗
    # =========================

    print("❌ 三次抓取全部失敗")

    return None
