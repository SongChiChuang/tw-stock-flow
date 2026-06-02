import os
import pandas as pd

from glob import glob


def analyze_foreign_accumulation():

    print("🟦 外資累積籌碼分析")

    files = sorted(
        glob(
            "data/*.csv"
        )
    )

    if len(files) < 14:

        print("❌ 資料不足14日")

        return

    target_files = files[-14:]

    print("📦 使用檔案:")

    for f in target_files:
        print(os.path.basename(f))

    stock_data = {}

    for idx, file in enumerate(target_files):

        try:

            df = pd.read_csv(
                file,
                encoding="utf-8-sig"
            )

            target_col = (
                "外陸資買賣超股數(不含外資自營商)"
            )

            for _, row in df.iterrows():

                stock_id = str(row["證券代號"])
                stock_name = str(row["證券名稱"])

                try:
                    value = float(
                        str(row[target_col]).replace(",", "")
                    )
                except:
                    value = 0

                if stock_id not in stock_data:

                    stock_data[stock_id] = {
                        "證券代號": stock_id,
                        "證券名稱": stock_name,
                        "buy_days": []
                    }

                if value > 0:

                    stock_data[stock_id][
                        "buy_days"
                    ].append(idx)

        except Exception as e:

            print(f"❌ 讀取失敗 {file}")
            print(e)

            return

    result = []

    for stock_id, info in stock_data.items():

        buy_days = sorted(
            info["buy_days"]
        )

        buy_count = len(
            buy_days
        )

        if buy_count < 10:
            continue

        streak = 0

        current = 13

        while current in buy_days:

            streak += 1
            current -= 1

        track = ""

        for i in range(14):

            if i in buy_days:
                track += "●"
            else:
                track += "○"

        result.append({

            "證券代號": info["證券代號"],
            "證券名稱": info["證券名稱"],
            "買進日數": buy_count,
            "軌跡": track,
            "_排序連買": streak

        })

    result_df = pd.DataFrame(
        result
    )

    if len(result_df) == 0:

        print("⚠️ 無符合條件個股")

        return

    result_df = result_df.sort_values(

        by=[
            "買進日數",
            "_排序連買"
        ],

        ascending=False

    )

    result_df = result_df.head(30)

    result_df.insert(

        0,

        "排名",

        range(
            1,
            len(result_df) + 1
        )

    )

    result_df = result_df.drop(
        columns=["_排序連買"]
    )

    os.makedirs(
        "reports/accumulation",
        exist_ok=True
    )

    output_path = (
        "reports/accumulation/"
        "foreign_accumulation_top30.csv"
    )

    result_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"✅ 已輸出: {output_path}"
    )
