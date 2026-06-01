import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_streak_chart():

    print("📈 產生外資連續買超圖表")

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

        plt.figure(
            figsize=(12, 8)
        )

        labels = (
            top20["證券名稱"]
            + "("
            + top20["證券代號"].astype(str)
            + ")"
        )

        plt.barh(
            labels,
            top20["總買超量"]
        )

        plt.title(
            "Foreign Buy Streak Top20"
        )

        plt.xlabel(
            "Total Buy Volume"
        )

        plt.tight_layout()

        save_path = (
            "docs/images/"
            "foreign_streak_top30.png"
        )

        plt.savefig(
            save_path,
            dpi=200,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"✅ 圖表已輸出: {save_path}"
        )

    except Exception as e:

        print("❌ 圖表產生失敗")

        print(e)
