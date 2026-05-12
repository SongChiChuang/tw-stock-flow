from datetime import datetime

# =========================================
# 是否為交易日
# =========================================

def is_trading_day():

    today = datetime.now()

    weekday = today.weekday()

    # 星期六 = 5
    # 星期日 = 6

    if weekday in [5, 6]:

        print("📅 今日為非交易日")

        return False

    print("📈 今日為交易日")

    return True
