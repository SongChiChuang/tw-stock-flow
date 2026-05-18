# utils/stock_filter.py

import re


# =========================
# ETF / 特殊商品關鍵字
# =========================

ETF_KEYWORDS = [
    "ETF",
    "反1",
    "反2",
    "槓桿",
    "正2",
    "高股息",
    "台灣50",
]


# =========================
# 判斷是否為有效股票
# =========================

def is_stock(stock_id, stock_name=""):

    # =========================
    # 強制轉字串
    # =========================

    stock_id = str(stock_id)

    stock_name = str(stock_name)

    # =========================
    # 去空白
    # =========================

    stock_id = stock_id.strip()

    stock_name = stock_name.strip()

    # =========================
    # 必須為4位數字
    # =========================

    if not re.fullmatch(r"\d{4}", stock_id):

        return False

    # =========================
    # 排除 ETF / 特殊商品
    # =========================

    for keyword in ETF_KEYWORDS:

        if keyword in stock_name:

            return False

    return True
