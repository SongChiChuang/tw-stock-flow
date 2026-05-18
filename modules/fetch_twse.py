# modules/fetch_twse.py

import os
import time
import requests
import pandas as pd
from io import StringIO
from datetime import datetime


TWSE_URL = (
    "https://www.twse.com.tw/rwd/zh/fund/T86"
    "?response=csv"
    "&date={date}"
    "&selectType=ALLBUT0999"
)

REQUIRED_COLUMN = "證券代號"


def fetch_twse_data():

    today = datetime.now().strftime("%Y%m%d")

    print("📅 今日交易日:", today)

    csv_text = None

    # =========================
    # 三次重試
    # =========================

    for i in range(3):

        print(f"🌐 第 {i+1} 次抓取")

        try:

            url = TWSE_URL.format(date=today)

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            # =========================
            # TWSE 正確編碼
            # =========================

            response.encoding = "cp950"

            raw_text = response.text

            print("========== TWSE RAW ==========")
            print(raw_text[:3000])
            print("========== END RAW ==========")

            # =========================
            # 基本有效性
            # =========================

            if REQUIRED_COLUMN not in raw_text:

                print("❌ 原始資料不含證券代號")

                time.sleep(3)

                continue

            csv_text = raw_text

            break

        except Exception as e:

            print("❌ 抓取失敗:", e)

            time.sleep(3)

    # =========================
    # 三次都失敗
    # =========================

    if csv_text is None:

        print("❌ 三次抓取全部失敗")

        return None

    # =========================
    # 清洗資料
    # =========================

    lines = csv_text.splitlines()

    clean_lines = []

    header_found = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # 找 header
        if REQUIRED_COLUMN in line:
            header_found = True

        if not header_found:
            continue

        # 排除垃圾行
        if "說明:" in line:
            continue

        if "ETF證券代號" in line:
            continue

        clean_lines.append(line)

    if len(clean_lines) <= 1:

        print("❌ 清洗後無有效資料")

        return None

    print("========== CLEAN CSV ==========")
    print("\n".join(clean_lines[:10]))
    print("========== END CLEAN ==========")

    # =========================
    # 建立 DataFrame
    # =========================

    try:

        clean_csv = "\n".join(clean_lines)

        df = pd.read_csv(
            StringIO(clean_csv)
        )

        print("✅ DataFrame建立成功")

    except Exception as e:

        print("❌ DataFrame建立失敗:", e)

        return None

    # =========================
    # 欄位清理
    # =========================

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    print("📋 DataFrame 欄位:")
    print(df.columns.tolist())

    if REQUIRED_COLUMN not in df.columns:

        print("❌ 找不到證券代號欄位")

        return None

    # =========================
    # 數值欄位清理
    # =========================

    for col in df.columns:

        try:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace('"', "", regex=False)
                .str.strip()
            )

        except:
            pass

    # =========================
    # 排除 ETF
    # =========================

    original_count = len(df)

    etf_keywords = [
        "ETF",
        "反1",
        "反2",
        "槓桿",
        "正2",
        "高股息",
        "台灣50"
    ]

    if "證券名稱" in df.columns:

        for keyword in etf_keywords:

            df = df[
                ~df["證券名稱"]
                .astype(str)
                .str.contains(keyword, na=False)
            ]

    removed_count = original_count - len(df)

    print(f"🧹 已排除ETF/特殊商品: {removed_count}")

    # =========================
    # 股票數量驗證
    # =========================

    print(f"📊 股票數量: {len(df)}")

    if len(df) < 100:

        print("❌ 股票數量異常過少")

        return None

    # =========================
    # 建立資料夾
    # =========================

    os.makedirs("data", exist_ok=True)

    # =========================
    # 儲存 CSV
    # =========================

    save_path = f"data/{today}.csv"

    try:

        df.to_csv(
            save_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"✅ 已儲存: {save_path}")

    except Exception as e:

        print("❌ CSV儲存失敗:", e)

        return None

    return save_path
