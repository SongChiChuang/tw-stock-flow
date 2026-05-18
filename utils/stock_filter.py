# utils/stock_filter.py
# =========================
# 股票過濾工具
# =========================

import re


# =========================
# ETF / 特殊商品關鍵字
# =========================
ETF_KEYWORDS = [
    "ETF",
    "反1",
    "反2",
    "正2",
    "槓桿",
    "期貨",
    "富邦VIX",
    "元大S&P",
    "國泰20年美債",
    "高股息",
    "科技ETF",
    "台灣50",
    "台灣50反1",
    "台灣50正2",
]


# =========================
# 判斷是否為有效上市股票
# =========================
def is_stock(stock_id, stock_name=""):

    stock_id = str(stock_id).strip()
    stock_name = str(stock_name).strip()

    # =========================
    # 必須是4位數字
    # 上市股票格式
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
