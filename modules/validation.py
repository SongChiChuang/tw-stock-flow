# modules/fetch_twse.py

import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime


def fetch_twse_data():

    url = (
        "https://www.twse.com.tw/rwd/zh/fund/T86"
        "?response=csv"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.encoding = "utf-8"

    raw_text = response.text

    print("========== TWSE RAW ==========")

    preview = "\n".join(raw_text.splitlines()[:20])

    print(preview)

    print("========== END RAW ==========")

    lines = raw_text.splitlines()

    cleaned_lines = []

    start_collect = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # 找到真正表頭
        if "證券代號" in line and "證券名稱" in line:
            start_collect = True

        if start_collect:
            cleaned_lines.append(line)

    if not cleaned_lines:
        raise Exception("TWSE無有效資料")

    csv_text = "\n".join(cleaned_lines)

    print("========== CLEAN CSV ==========")
    print("\n".join(cleaned_lines[:5]))
    print("========== END CLEAN ==========")

    df = pd.read_csv(StringIO(csv_text))

    print("✅ DataFrame建立成功")

    today = datetime.now().strftime("%Y%m%d")

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / f"{today}.csv"

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✅ 已儲存: {output_path}")

    return df
