      # =========================
      # 從 TWSE 抓資料
      # =========================
import requests
import pandas as pd
from io import StringIO
from datetime import datetime


def fetch_twse_data():

    today = datetime.now().strftime("%Y%m%d")

    url = (
        "https://www.twse.com.tw/"
        f"fund/T86?response=csv&date={today}&selectType=ALLBUT0999"
    )

    response = requests.get(url)

    response.encoding = "cp950"

    lines = response.text.split("\n")

    start = 0

    for i, line in enumerate(lines):

        if "證券代號" in line:
            start = i
            break

    csv_text = "\n".join(lines[start:])

    df = pd.read_csv(StringIO(csv_text))

    df.columns = df.columns.str.strip()

    print("📥 資料已更新")
    print("✅ TWSE資料抓取成功")

    return df, today
