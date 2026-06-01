import os
import pandas as pd

from glob import glob

def analyze_foreign_streak():

print("🔥 外資連續買超分析")

# =========================
# 最近五日 TOP30
# =========================

files = sorted(
    glob(
        "reports/foreign/*_foreign_buy_top30.csv"
    )
)

if len(files) < 5:

    print("❌ TOP30資料不足")

    return

target_files = files[-5:]

print("📦 使用檔案:")

for f in target_files:
    print(os.path.basename(f))

# =========================
# 日期權重
# =========================

date_weights = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 5
}

stock_data = {}

# =========================
# 讀取五日資料
# =========================

for idx, file in enumerate(target_files):

    try:

        df = pd.read_csv(
            file,
            encoding="utf-8-sig"
        )

        weight = date_weights[idx]

        for _, row in df.iterrows():

            stock_id = str(row["證券代號"])

            stock_name = str(row["證券名稱"])

            volume = float(
                str(row["外資買賣超股數"])
                .replace(",", "")
            )

            if stock_id not in stock_data:

                stock_data[stock_id] = {
                    "證券代號": stock_id,
                    "證券名稱": stock_name,
                    "日期權重": 0,
                    "上榜次數": 0,
                    "五日總買超": 0,
                    "days": []
                }

            stock_data[stock_id]["日期權重"] += weight

            stock_data[stock_id]["上榜次數"] += 1

            stock_data[stock_id]["五日總買超"] += volume

            stock_data[stock_id]["days"].append(idx)

    except Exception as e:

        print(f"❌ 讀取失敗 {file}")

        print(e)

        return

# =========================
# 最近連續天數
# =========================

result = []

for stock_id, info in stock_data.items():

    days = sorted(info["days"])

    streak = 0

    current = 4

    while current in days:

        streak += 1
        current -= 1

    # =========================
    # 軌跡
    # =========================

    track = ""

    for i in range(5):

        if i in days:
            track += "●"
        else:
            track += "○"

    result.append({

        "證券代號": info["證券代號"],
        "證券名稱": info["證券名稱"],

        "軌跡": track,

        "日期權重": info["日期權重"],
        "上榜次數": info["上榜次數"],
        "最近連續": streak,

        "熱度": "★" * streak,

        "五日總買超": int(
            info["五日總買超"]
        )
    })

# =========================
# DataFrame
# =========================

result_df = pd.DataFrame(result)

result_df = result_df.sort_values(
    by=[
        "日期權重",
        "上榜次數",
        "最近連續",
        "五日總買超"
    ],
    ascending=False
)

result_df = result_df.head(30)

# =========================
# 排名
# =========================

result_df.insert(
    0,
    "排名",
    range(1, len(result_df) + 1)
)

# =========================
# 輸出
# =========================

os.makedirs(
    "reports/streak",
    exist_ok=True
)

output_path = (
    "reports/streak/"
    "foreign_streak_top30.csv"
)

result_df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print(f"✅ 已輸出: {output_path}")
