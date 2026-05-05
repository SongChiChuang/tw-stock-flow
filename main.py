import requests
import pandas as pd
from io import StringIO

url = "https://www.twse.com.tw/rwd/zh/fund/T86?date=20260421&selectType=ALLBUT0999&response=csv"

res = requests.get(url)
text = res.text

lines = []
for line in text.split("\n"):
    if "證券代號" in line or line.startswith('"'):
        lines.append(line)

csv_data = "\n".join(lines)

df = pd.read_csv(StringIO(csv_data))

print(df.head())
