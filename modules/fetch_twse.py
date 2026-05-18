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

    preview = "\n".join(raw_text.splitlines()[:40])

    print(preview)

    print("========== END RAW ==========")

    lines = raw_text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # 保留表頭
        if "證券代號" in line and "證券名稱" in line:
            cleaned_lines.append(line)
            continue

        # 保留股票資料列
        if line.startswith('"'):
            cleaned_lines.append(line)

    if len(cleaned_lines) <= 1:
        raise Exception("TWSE無有效股票資料")

    csv_text = "\n".join(cleaned_lines)

    print("========== CLEAN CSV ==========")

    preview_clean = "\n".join(cleaned_lines[:10])

    print(preview_clean)

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
