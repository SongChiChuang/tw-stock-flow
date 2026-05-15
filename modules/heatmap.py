import pandas as pd
from pathlib import Path

OUTPUT_HTML = "docs/index.html"

# =========================
# 讀取 CSV
# =========================

def load_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"❌ CSV讀取失敗: {path}")
        print(e)
        return pd.DataFrame()

# =========================
# 安全取得欄位
# =========================

def get_value(row, columns):
    for col in columns:
        if col in row:
            return row[col]
    return ""

# =========================
# 建立表格 HTML
# =========================

def build_table(title, df):

    if df.empty:
        return f"""
        <div class="card">
            <h2>{title}</h2>
            <p>無資料</p>
        </div>
        """

    html = f"""
    <div class="card">
        <h2>{title}</h2>

        <table>
            <thead>
                <tr>
                    <th>排名</th>
                    <th>股票代號</th>
                    <th>股票名稱</th>
                    <th>買賣超</th>
                </tr>
            </thead>

            <tbody>
    """

    for idx, row in df.head(30).iterrows():

        stock_id = get_value(row, [
            "證券代號",
            "股票代號"
        ])

        stock_name = get_value(row, [
            "證券名稱",
            "股票名稱"
        ])

        volume = get_value(row, [
            "買賣超股數",
            "買賣超",
            "買超"
        ])

        # 數字格式化
        try:
            volume = format(int(float(volume)), ",")
        except:
            volume = str(volume)

        html += f"""
        <tr>
            <td>{idx + 1}</td>
            <td>{stock_id}</td>
            <td>{stock_name}</td>
            <td>{volume}</td>
        </tr>
        """

    html += """
            </tbody>
        </table>
    </div>
    """

    return html

# =========================
# 主程式
# =========================

def generate_heatmap():

    foreign_buy = load_csv("reports/foreign_buy_30.csv")
    foreign_sell = load_csv("reports/foreign_sell_30.csv")
    investment_buy = load_csv("reports/investment_buy_30.csv")
    investment_sell = load_csv("reports/investment_sell_30.csv")

    html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

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
每日自動更新
</div>

{build_table("外資買超 TOP30", foreign_buy)}

{build_table("外資賣超 TOP30", foreign_sell)}

{build_table("投信買超 TOP30", investment_buy)}

{build_table("投信賣超 TOP30", investment_sell)}

</body>
</html>
"""

    Path("docs").mkdir(exist_ok=True)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ heatmap html 生成完成")

# =========================

if __name__ == "__main__":
    generate_heatmap()
