# modules/fetch_twse.py

import os
import time
import requests
import pandas as pd

from datetime import datetime


# =========================
# TWSE JSON API
# =========================

TWSE_URL = (
    "https://www.twse.com.tw/rwd/zh/fund/T86"
    "?response=json"
    "&date={date}"
    "&selectType=ALLBUT0999"
)

REQUIRED_COLUMN = "證券代號"


def fetch_twse_data():

    today = datetime.now().strftime("%Y%m%d")

    print("📅 今日交易日:", today)

    df = None

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
                    " AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                ),
                "Referer": "https://www.twse.com.tw/",
                "Accept-Language": "zh-TW,zh;q=0.9"
            }

            # =========================
            # Session Retry
            # =========================

            session = requests.Session()

            adapter = requests.adapters.HTTPAdapter(
                max_retries=5
            )

            session.mount(
                "https://",
                adapter
            )

            # =========================
            # Request
            # =========================

            response = session.get(
                url,
                headers=headers,
                timeout=120
            )

            print("========== RESPONSE ==========")
            print(response.text[:1000])
            print("========== END RESPONSE ==========")

            # =========================
            # JSON
            # =========================

            data = response.json()

            # =========================
            # 檢查資料
            # =========================

            if "data" not in data:

                print("❌ JSON無 data 欄位")

                time.sleep(5)

                continue

            if len(data["data"]) == 0:

                print("❌ 今日無資料")

                time.sleep(5)

                continue

            # =========================
            # 建立 DataFrame
            # =========================

            df = pd.DataFrame(
                data["data"],
                columns=data["fields"]
            )

            print("✅ DataFrame建立成功")

            break

        except Exception as e:

            print("❌ 抓取失敗:", e)

            time.sleep(10)

    # =========================
    # 三次都失敗
    # =========================

    if df is None:

        print("❌ 三次抓取全部失敗")

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
    # 排除 ETF / 特殊商品
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
