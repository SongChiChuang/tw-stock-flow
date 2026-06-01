import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_streak_chart():

    print("📈 產生外資五日強勢排行榜")

    try:

        csv_path = (
            "reports/streak/"
            "foreign_streak_top30.csv"
        )

        if not os.path.exists(csv_path):

            print("❌ 找不到 foreign_streak_top30.csv")
            return

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        if len(df) == 0:

            print("❌ 無資料")
            return

        top20 = df.head(20)

        os.makedirs(
            "docs/images",
            exist_ok=True
        )

        fig, ax = plt.subplots(
            figsize=(16, 10)
        )

        ax.axis("off")

        title = (
            "Foreign Buy Streak Ranking"
        )

        plt.title(
            title,
            fontsize=20,
            pad=20
        )

        table_data = []

        for _, row in top20.iterrows():

            table_data.append([

                row["排名"],
                row["證券代號"],
                row["證券名稱"],
                row["日期權重"],
                row["上榜次數"],
                row["最近連續"],
                f"{int(row['五日總買超']):,}"

            ])

        table = ax.table(

            cellText=table_data,

            colLabels=[

                "Rank",
                "Code",
                "Name",
                "Date",
                "Count",
                "Streak",
                "Volume"

            ],

            loc="center"

        )

        table.auto_set_font_size(
            False
        )

        table.set_fontsize(
            10
        )

        table.scale(
            1.2,
            1.8
        )

        save_path = (
            "docs/images/"
            "foreign_streak_top30.png"
        )

        plt.savefig(
            save_path,
            dpi=250,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"✅ 圖表已輸出: {save_path}"
        )

    except Exception as e:

        print("❌ 圖表產生失敗")
        print(e)
