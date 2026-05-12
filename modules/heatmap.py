import os

from utils.config import TOP_N

from utils.stock_filter import (
    filter_stocks
)

# =========================================
# 共用 Heatmap Function
# =========================================

def generate_heatmap(

    df,
    today_str,
    column_name,
    output_name,
    ascending=False

):

    print(f"\n📊 產生 {output_name}")

    # =====================================
    # 統一股票過濾
    # =====================================

    stock_df = filter_stocks(df)

    # =====================================
    # 排序
    # =====================================

    stock_df = stock_df.sort_values(
        by=column_name,
        ascending=ascending
    )

    # =====================================
    # Top N
    # =====================================

    top_n = stock_df.head(TOP_N)

    # =====================================
    # 輸出欄位
    # =====================================

    output_df = top_n[[

        "證券代號",
        "證券名稱",
        column_name

    ]]

    # =====================================
    # 建立資料夾
    # =====================================

    os.makedirs(
        "reports/heatmap",
        exist_ok=True
    )

    # =====================================
    # 存檔
    # =====================================

    filename = (
        f"reports/heatmap/"
        f"{today_str}_{output_name}.csv"
    )

    output_df.to_csv(
        filename,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✅ 已輸出: {filename}")

# =========================================
# 外資買超
# =========================================

def generate_foreign_buy_top30(
    df,
    today_str
):

    generate_heatmap(

        df=df,

        today_str=today_str,

        column_name=(
            "外陸資買賣超股數(不含外資自營商)"
        ),

        output_name="foreign_buy_30",

        ascending=False
    )

# =========================================
# 外資賣超
# =========================================

def generate_foreign_sell_top30(
    df,
    today_str
):

    generate_heatmap(

        df=df,

        today_str=today_str,

        column_name=(
            "外陸資買賣超股數(不含外資自營商)"
        ),

        output_name="foreign_sell_30",

        ascending=True
    )

# =========================================
# 投信買超
# =========================================

def generate_trust_buy_top30(
    df,
    today_str
):

    generate_heatmap(

        df=df,

        today_str=today_str,

        column_name="投信買賣超股數",

        output_name="trust_buy_30",

        ascending=False
    )

# =========================================
# 投信賣超
# =========================================

def generate_trust_sell_top30(
    df,
    today_str
):

    generate_heatmap(

        df=df,

        today_str=today_str,

        column_name="投信買賣超股數",

        output_name="trust_sell_30",

        ascending=True
    )
