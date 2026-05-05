import requests
import pandas as pd
from io import StringIO
from datetime import datetime

# ========= 設定日期 =========
date_str = "20260421"  # 之後可以改成自動

url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={date_str}&selectType=ALLBUT0999&response=csv"

res = requests.get(url)
text = res.text

# ========= 清理CSV =========
lines = []
for line in text.split("\n"):
    if "證券代號" in line or line.startswith('"'):
        lines.append(line)

csv_data = "\n".join(lines)

df = pd.read_csv(StringIO(csv_data))

# ========= 存檔 =========
today = datetime.today().strftime("%Y-%m-%d")

filename = f"data_{today}.csv"
df.to_csv(filename, index=False)

print("✅ 已成功執行並存檔:", filename)
print(df.head())
