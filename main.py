import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os
import time

# ========= 日期 =========
today_str = datetime.today().strftime("%Y%m%d")

url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={today_str}&selectType=ALLBUT0999&response=csv"

# ========= 🔥 重試機制 =========
for i in range(5):  # 最多等5次（約5分鐘）
    res = requests.get(url)
    text = res.text

    if "證券代號" in text:
        print("✅ 資料已取得")
        break
    else:
        print(f"⏳ 第{i+1}次：資料尚未更新，等待1分鐘...")
        time.sleep(60)
else:
    print("❌ 今日資料最終仍未更新，結束")
    exit()

# ========= 解析資料 =========
lines = text.split("\n")

start = 0
for i, line in enumerate(lines):
    if "證券代號" in line:
        start = i
        break

clean_data = "\n".join(lines[start:])

df = pd.read_csv(StringIO(clean_data))

# ========= 存檔 =========
os.makedirs("data", exist_ok=True)

filename = f"data/{today_str}.csv"
df.to_csv(filename, index=False)

print("✅ 已儲存:", filename)
print(df.head())
