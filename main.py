import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import os

# ========= 日期（自動抓今天）=========
today_str = datetime.today().strftime("%Y%m%d")

url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={today_str}&selectType=ALLBUT0999&response=csv"

res = requests.get(url)
text = res.text

# ========= 清理 CSV =========
lines = []
for line in text.split("\n"):
    if "證券代號" in line or line.startswith('"'):
        lines.append(line)

csv_data = "\n".join(lines)

df = pd.read_csv(StringIO(csv_data))

# ========= 建資料夾 =========
os.makedirs("data", exist_ok=True)

# ========= 存檔 =========
filename = f"data/{today_str}.csv"
df.to_csv(filename, index=False)

print("✅ 已儲存:", filename)
