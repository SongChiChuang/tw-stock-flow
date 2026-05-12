from utils.code_utils import (
    normalize_stock_code
)

# =========================================
# ETF / 槓反 / 基金 過濾
# =========================================

ETF_KEYWORDS = [

    "ETF",
    "反1",
    "反2",
    "正2",
    "槓桿",
    "期街口",
    "富邦VIX"

]

# =========================================
# 股票過濾
# =========================================

def filter_stocks(df):

    stock_df = df.copy()

    # =====================================
    # 股票代號標準化
    # =====================================

    stock_df["證券代號"] = (

        stock_df["證券代號"]
        .apply(normalize_stock_code)

    )

    # =====================================
    # 名稱過濾
    # =====================================

    for keyword in ETF_KEYWORDS:

        stock_df = stock_df[
            ~stock_df["證券名稱"]
            .astype(str)
            .str.contains(
                keyword,
                na=False
            )
        ]

    # =====================================
    # ETF代號過濾
    # =====================================

    stock_df = stock_df[

        ~stock_df["證券代號"]
        .astype(str)
        .str.startswith("00")

    ]

    return stock_df
