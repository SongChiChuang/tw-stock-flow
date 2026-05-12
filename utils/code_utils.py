# =========================================
# 股票代號標準化
# =========================================

def normalize_stock_code(code):

    # 轉字串

    code = str(code)

    # 去除 ="2330"

    code = code.replace('="', '')
    code = code.replace('"', '')

    # 去空白

    code = code.strip()

    return code
