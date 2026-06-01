
import pandas as pd
import os


def dataframe_to_html(df):

    html = "<table>"

    html += "<tr>"

    for col in df.columns:

        html += f"<th>{col}</th>"

    html += "</tr>"

    for _, row in df.iterrows():

        html += "<tr>"

        for value in row:

            html += f"<td>{value}</td>"

        html += "</tr>"

    html += "</table>"

    return html


def generate_dashboard(csv_path):

    print("📊 產生 Dashboard")

    try:

        file_date = os.path.basename(
            csv_path
        ).replace(".csv", "")

        # =========================
        # CSV 路徑
        # =========================

        foreign_buy_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_buy_top30.csv"
        )

        foreign_sell_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_sell_top30.csv"
        )

        investment_buy_path = (
            f"reports/investment/"
            f"{file_date}_investment_buy_top30.csv"
        )

        investment_sell_path = (
            f"reports/investment/"
            f"{file_date}_investment_sell_top30.csv"
        )

        streak_path = (
            "reports/streak/"
            "foreign_streak_top30.csv"
        )

        # =========================
        # 讀CSV
        # =========================

        foreign_buy = pd.read_csv(
            foreign_buy_path,
            encoding="utf-8-sig"
        )

        foreign_sell = pd.read_csv(
            foreign_sell_path,
            encoding="utf-8-sig"
        )

        investment_buy = pd.read_csv(
            investment_buy_path,
            encoding="utf-8-sig"
        )

        investment_sell = pd.read_csv(
            investment_sell_path,
            encoding="utf-8-sig"
        )

        if os.path.exists(streak_path):

            streak_df = pd.read_csv(
                streak_path,
                encoding="utf-8-sig"
            )

        else:

            streak_df = pd.DataFrame({
                "訊息": ["尚無資料"]
            })

        # =========================
        # 轉HTML
        # =========================

        foreign_buy_html = dataframe_to_html(
            foreign_buy
        )

        foreign_sell_html = dataframe_to_html(
            foreign_sell
        )

        investment_buy_html = dataframe_to_html(
            investment_buy
        )

        investment_sell_html = dataframe_to_html(
            investment_sell
        )

        streak_html = dataframe_to_html(
            streak_df
        )

        # =========================
        # HTML
        # =========================

        html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>TW Stock Flow Dashboard</title>

<style>

body {{
    background: #050816;
    color: white;
    font-family: Arial;
    margin: 0;
    padding: 20px;
}}

h1 {{
    color: #00ff99;
    font-size: 56px;
    margin-bottom: 10px;
}}

.subtitle {{
    color: #888;
    margin-bottom: 40px;
}}

.card {{
    background: #111827;
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 40px;
    overflow-x: auto;
}}

h2 {{
    font-size: 42px;
    margin-bottom: 24px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    color: #00ff99;
    font-size: 28px;
    padding: 18px;
    border-bottom: 1px solid #333;
}}

td {{
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #222;
    font-size: 28px;
}}

@media screen and (max-width: 768px) {{

    h1 {{
        font-size: 28px;
    }}

    h2 {{
        font-size: 22px;
    }}

    th {{
        font-size: 16px;
        padding: 10px;
    }}

    td {{
        font-size: 16px;
        padding: 12px;
    }}

}}

</style>

</head>

<body>

<h1>TW Stock Flow Dashboard</h1>

<div class="subtitle">
每日自動更新 - {file_date}
</div>

<div class="card">
<h2>外資買超 TOP30</h2>
{foreign_buy_html}
</div>

<div class="card">
<h2>外資賣超 TOP30</h2>
{foreign_sell_html}
</div>

<div class="card">
<h2>投信買超 TOP30</h2>
{investment_buy_html}
</div>

<div class="card">
<h2>投信賣超 TOP30</h2>
{investment_sell_html}
</div>

<div class="card">
<h2>🔥 外資持續熱度榜</h2>
{streak_html}
</div>

<div class="card">
<h2>外資五日連續買超排行榜</h2>

<img
src="images/foreign_streak_top30.png"
style="
width:100%;
border-radius:20px;
background:white;
padding:10px;
"
/>

</div>

</body>
</html>
"""

        os.makedirs(
            "docs",
            exist_ok=True
        )

        with open(
            "docs/index.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        print("✅ Dashboard 已更新")

    except Exception as e:

        print("❌ Dashboard生成失敗")

        print(e)
