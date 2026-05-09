import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os
import time
import sys

# ========= 時間設定 =========

START_HOUR = 16
END_HOUR = 21

# 16:00~18:00 每30分鐘
EARLY_INTERVAL = 1800

# 18:00~21:00 每10分鐘
LATE_INTERVAL = 600

# ========= 日期 =========

today_str = datetime.today().strftime("%Y%m%d")

url = (
    "https://www.twse.com.tw/rwd/zh/fund/T86"
    f"?date={today_str}&selectType=ALLBUT0999&response=csv"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ========= 等待資料 =========

text = None

while True:

    now = datetime.now()

    current_hour = now.hour

    # ========= 超過21:00結束 =========

    if current_hour >= END_HOUR:

        print("❌ 已超過21:00，今日資料仍未更新")

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

            # ========= cp950 解碼 =========

            text = res.content.decode(
                "cp950",
                errors="replace"
            )

            # ========= 資料已更新 =========

            if "證券代號" in text:

                print("✅ 資料已更新")

                break

            print("⏳ 資料尚未更新")

    except Exception as e:

        print(f"❌ 抓取失敗: {e}")

    # ========= 動態等待 =========

    if current_hour < 18:

        wait_time = EARLY_INTERVAL

        print("🕒 30分鐘後重試")

    else:

        wait_time = LATE_INTERVAL

        print("🕒 10分鐘後重試")

    time.sleep(wait_time)

# ========= 自動定位表頭 =========

lines = text.splitlines()

header_index = None

for i, line in enumerate(lines):

    if "證券代號" in line and "證券名稱" in line:

        header_index = i

        break

if header_index is None:

    print("❌ 找不到表頭")

    sys.exit(1)

csv_text = "\n".join(lines[header_index:])

# ========= CSV解析 =========

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

# ========= 移除空白列 =========

df = df.dropna(how="all")

# ========= 驗證欄位 =========

expected_columns = len(df.columns)

for idx, row in df.iterrows():

    if len(row) != expected_columns:

        print(f"❌ 欄位錯位: 第 {idx} 列")

        sys.exit(1)

# ========= 清理欄位名稱 =========

df.columns = [str(c).strip() for c in df.columns]

# ========= 清理文字 =========

def clean_text(x):

    if pd.isna(x):
        return ""

    x = str(x)

    x = x.replace('="', '')
    x = x.replace('"', '')
    x = x.strip()

    return x

for col in df.columns:

    df[col] = df[col].apply(clean_text)

# ========= 數值欄位 =========

numeric_columns = [

    col for col in df.columns

    if any(keyword in col for keyword in [

        "買進股數",
        "賣出股數",
        "買賣超股數"

    ])
]

for col in numeric_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .replace("", "0")
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)

# ========= 建立資料夾 =========

os.makedirs("data", exist_ok=True)

# ========= 存檔 =========

filename = f"data/{today_str}.csv"

df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
)

print(f"\n✅ 已儲存: {filename}")

print("\n===================")
print("資料驗證成功")
print("===================")

print(df.head())
