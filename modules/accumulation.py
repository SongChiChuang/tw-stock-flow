# modules/accumulation.py

import pandas as pd
from pathlib import Path


def analyze_foreign_accumulation():

    print("📈 外資累積買超分析")

    data_dir = Path("data")

    csv_files = sorted(
        data_dir.glob("*.csv")
    )

    if len(csv_files) < 10:

        print("❌ CSV檔案不足")

        return

    target_files = csv_files[-10:]

    all_data = []

    for file in target_files:

        try:

            # =========================
            # UTF-8-SIG
            # =========================

            df = pd.read_csv(
                file,
                encoding="utf-8-sig"
            )

            print(f"✅ 已讀取: {file.name}")

            all_data.append(df)

        except Exception as e:

            print(f"❌ 讀取失敗 {file.name}: {e}")

            return

    print("✅ 累積分析完成")
