# =========================
# 排除 ETF / 特殊商品
# =========================

original_count = len(df)

# ETF / ETN / 債券 / 槓反 / 主動ETF 關鍵字

etf_keywords = [

    "ETF",
    "ETN",

    "反1",
    "反2",
    "正2",

    "槓桿",
    "期貨",

    "高股息",
    "高息",

    "債",
    "美債",
    "公司債",

    "台灣50",
    "臺灣50",

    "NASDAQ",
    "納斯達克",

    "S&P",
    "半導體",

    "科技優息",
    "精選高息",

    "主動",
]

filtered_rows = []

removed_count = 0

if "證券名稱" in df.columns:

    for row in df.values.tolist():

        stock_id = str(row[0]).strip()

        stock_name = str(row[1]).strip()

        # =========================
        # 規則1：
        # 00開頭直接排除
        # =========================

        if stock_id.startswith("00"):

            removed_count += 1

            continue

        # =========================
        # 規則2：
        # 名稱關鍵字排除
        # =========================

        is_etf = any(
            keyword in stock_name
            for keyword in etf_keywords
        )

        if is_etf:

            removed_count += 1

            continue

        filtered_rows.append(row)

    df = pd.DataFrame(
        filtered_rows,
        columns=df.columns
    )

else:

    print("⚠️ 找不到證券名稱欄位")

removed_count = original_count - len(df)

print(f"🧹 已排除ETF/特殊商品: {removed_count}")
