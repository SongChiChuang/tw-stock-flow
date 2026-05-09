from modules.fetch_twse import fetch_twse_data
df = fetch_twse_data()

print(df.head())

import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os
import time
import sys
import re

# =========================================
# 時間設定
# =========================================

START_HOUR = 16
END_HOUR = 21

EARLY_INTERVAL = 1800
LATE_INTERVAL = 600

# =========================================
# 日期
# =========================================

today = datetime.now()

today_str = today.strftime("%Y%m%d")

url = (
    "https://www.twse.com.tw/rwd/zh/fund/T86"
    f"?date={today_str}&selectType=ALLBUT0999&response=csv"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# =========================================
# Validation Report
# =========================================

validation_logs = []

def add_pass(msg):

    validation_logs.append(f"[PASS] {msg}")

    print(f"✅ {msg}")

def add_warning(msg):

    validation_logs.append(f"[WARNING] {msg}")

    print(f"⚠️ WARNING: {msg}")

def add_fail(msg):

    validation_logs.append(f"[FAIL] {msg}")

    print(f"❌ FAIL: {msg}")

    save_validation_report()

    sys.exit(1)

def save_validation_report():

    os.makedirs("reports", exist_ok=True)

    report_path = f"reports/{today_str}_validation.txt"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(validation_logs))

# =========================================
# 等待資料
# =========================================

text = None

while True:

    now = datetime.now()

    current_hour = now.hour

    if current_hour >= END_HOUR:

        add_fail("已超過21:00仍未取得資料")

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

            text = res.content.decode(
                "cp950",
                errors="replace"
            )

            if "證券代號" in text:

                print("✅ 資料已更新")

                break

            print("⏳ 資料尚未更新")

    except Exception as e:

        print(f"❌ 抓取失敗: {e}")

    if current_hour < 18:

        print("🕒 30分鐘後重試")

        time.sleep(EARLY_INTERVAL)

    else:

        print("🕒 10分鐘後重試")

        time.sleep(LATE_INTERVAL)

# =========================================
# 定位表頭
# =========================================

lines = text.splitlines()

header_index = None

for i, line in enumerate(lines):

    if "證券代號" in line and "證券名稱" in line:

        header_index = i

        break

if header_index is None:

    add_fail("找不到表頭")

csv_text = "\n".join(lines[header_index:])

# =========================================
# CSV解析
# =========================================

try:

    df = pd.read_csv(
        StringIO(csv_text),
        encoding="cp950",
        thousands=",",
        dtype=str
    )

    add_pass("CSV解析成功")

except Exception as e:

    add_fail(f"CSV解析失敗: {e}")

# =========================================
# 移除空白列
# =========================================

df = df.dropna(how="all")

# =========================================
# 欄位數驗證
# =========================================

expected_columns = len(df.columns)

for idx, row in df.iterrows():

    if len(row) != expected_columns:

        add_fail(f"欄位錯位: 第 {idx} 列")

add_pass("欄位數一致")

# =========================================
# 清理欄位名稱
# =========================================

df.columns = [str(c).strip() for c in df.columns]

# =========================================
# 必要欄位驗證
# =========================================

required_columns = [

    "證券代號",
    "證券名稱",
    "外陸資買賣超股數(不含外資自營商)",
    "投信買賣超股數"

]

for col in required_columns:

    if col not in df.columns:

        add_fail(f"缺少必要欄位: {col}")

add_pass("必要欄位完整")

# =========================================
# row count validation
# =========================================

row_count = len(df)

if row_count < 1000:

    add_fail(f"股票數量異常: {row_count}")

add_pass(f"股票數量正常: {row_count}")

# =========================================
# 清理文字
# =========================================

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

# =========================================
# 股票代號格式驗證
# =========================================

stock_pattern = re.compile(r"^[0-9A-Z]{4,6}$")

invalid_codes = []

for code in df["證券代號"]:

    if not stock_pattern.match(str(code)):

        invalid_codes.append(code)

if len(invalid_codes) > 0:

    add_warning(
        f"發現異常股票代號: {invalid_codes[:10]}"
    )

else:

    add_pass("股票代號格式正常")

# =========================================
# duplicate驗證
# =========================================

duplicate_codes = df[
    df["證券代號"].duplicated()
]

if len(duplicate_codes) > 0:

    add_fail("發現重複股票代號")

add_pass("無重複股票代號")

# =========================================
# 數值欄位
# =========================================

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

add_pass("數值欄位轉換完成")

# =========================================
# 異常值 Warning
# =========================================

warning_threshold = 300000000

foreign_col = "外陸資買賣超股數(不含外資自營商)"

abnormal_df = df[
    abs(df[foreign_col]) > warning_threshold
]

if len(abnormal_df) > 0:

    add_warning(
        f"發現異常大買賣超股票數量: {len(abnormal_df)}"
    )

else:

    add_pass("未發現異常大買賣超")

# =========================================
# 歷史row count比較
# =========================================

history_files = sorted(os.listdir("data")) if os.path.exists("data") else []

if len(history_files) >= 1:

    latest_file = history_files[-1]

    try:

        old_df = pd.read_csv(
            f"data/{latest_file}"
        )

        old_count = len(old_df)

        diff_ratio = abs(
            row_count - old_count
        ) / old_count

        if diff_ratio > 0.2:

            add_warning(
                f"股票數量較前次變動超過20% "
                f"(舊:{old_count} 新:{row_count})"
            )

        else:

            add_pass("股票數量波動正常")

    except:

        add_warning("歷史資料比較失敗")

# =========================================
# 建立資料夾
# =========================================

os.makedirs("data", exist_ok=True)

# =========================================
# 存檔
# =========================================

filename = f"data/{today_str}.csv"

df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
)

add_pass(f"資料已儲存: {filename}")

# =========================================
# 儲存 validation report
# =========================================

save_validation_report()

print("\n===================")
print("Validation 完成")
print("===================")
