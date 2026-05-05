import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os

# ========= 日期 =========
today_str = datetime.today().strftime("%Y%m%d")

url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={today_str}&selectType=ALLBUT0999&response=csv"

res = requests.get(url)
text = res.text

# ========= 🔥 穩定解析 =========
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
