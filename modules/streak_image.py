# modules/streak_image.py

import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_streak_image():

    print("🖼️ 產生外資熱度榜圖片")

    csv_path = (
        "reports/streak/"
        "foreign_streak_top30.csv"
    )

    if not os.path.exists(csv_path):

        print("❌ 找不到 streak csv")

        return

    try:

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        # =========================
        # 只保留前15
        # =========================

        df = df.head(15)

        # =========================
        # 圖片大小
        # =========================

        fig_height = len(df) * 0.55 + 2

        fig, ax = plt.subplots(
            figsize=(14, fig_height)
        )

        ax.axis("off")

        # =========================
        # 表格內容
        # =========================

        columns = [
            "排名",
            "證券代號",
            "證券名稱",
            "上榜次數",
            "最近連續",
            "日期權重",
            "五日總買超"
        ]

        table = ax.table(
            cellText=df[columns].values,
            colLabels=columns,
            loc="center",
            cellLoc="center"
        )

        # =========================
        # 字體
        # =========================

        table.auto_set_font_size(False)

        table.set_fontsize(12)

        table.scale(1, 1.7)

        # =========================
        # 標題
        # =========================

        plt.title(
            "Foreign Streak TOP30",
            fontsize=22,
            pad=20
        )

        # =========================
        # 輸出資料夾
        # =========================

        os.makedirs(
            "docs/images",
            exist_ok=True
        )

        output_path = (
            "docs/images/"
            "foreign_streak_top30.png"
        )

        plt.savefig(
            output_path,
            bbox_inches="tight",
            dpi=200
        )

        plt.close()

        print(f"✅ 已輸出圖片: {output_path}")

    except Exception as e:

        print("❌ 圖片產生失敗")

        print(e)
