import pandas as pd
import os


def generate_accumulation(min_days=5):

    print(f"📈 外資連續買超分析（>= {min_days} 日）")

    data_dir = "data"

    csv_files = sorted([
        f for f in os.listdir(data_dir)
        if f.endswith(".csv")
    ])

    csv_files = csv_files[-5:]

    print(f"📂 使用資料: {csv_files}")

    dfs = []

    for file in csv_files:

        path = os.path.join(data_dir, file)

        df = pd.read_csv(path)

        df["資料日期"] = file.replace(".csv", "")

        dfs.append(df)

        print(f"✅ 已讀取: {file}")

    combined = pd.concat(dfs)

    print(f"✅ 合併完成（總筆數: {len(combined)}）")

    # =========================
    # 外資買賣超欄位
    # =========================

    target_col = "外陸資買賣超股數(不含外資自營商)"

    if target_col not in combined.columns:

        print("❌ 找不到外資買賣超欄位")
        return

    combined[target_col] = (
        combined[target_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    combined[target_col] = pd.to_numeric(
        combined[target_col],
        errors="coerce"
    ).fillna(0)

    # =========================
    # 每日外資 > 0
    # =========================

    positive = combined[
        combined[target_col] > 0
    ]

    grouped = positive.groupby(
        ["證券代號", "證券名稱"]
    ).size().reset_index(name="買超天數")

    result = grouped[
        grouped["買超天數"] >= min_days
    ]

    result = result.sort_values(
        by="買超天數",
        ascending=False
    )

    # =========================
    # 輸出
    # =========================

    latest_date = csv_files[-1].replace(".csv", "")

    output_dir = "reports/accumulation"

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        f"{latest_date}_foreign_accumulation.csv"
    )

    result.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✅ 已輸出: {output_path}")

    print(result.head())

    return result
