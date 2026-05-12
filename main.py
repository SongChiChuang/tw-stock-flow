from datetime import datetime

from modules.fetch_twse import fetch_twse_data
from modules.validation import validate_dataframe
from modules.cleanup import cleanup_old_data
from modules.heatmap import generate_foreign_buy_top30
from modules.trading_calendar import is_trading_day

# =========================================
# 今日日期
# =========================================

today_str = datetime.now().strftime(
    "%Y%m%d"
)

# =========================================
# 交易日判斷
# =========================================

if not is_trading_day():

    print("⏹️ 非交易日，結束系統")

    exit()

# =========================================
# 抓取 TWSE 資料
# =========================================

df = fetch_twse_data()

# =========================================
# Validation
# =========================================

df = validate_dataframe(
    df,
    today_str=today_str
)

# =========================================
# 儲存原始資料
# =========================================

raw_filename = f"data/{today_str}.csv"

df.to_csv(
    raw_filename,
    index=False,
    encoding="utf-8-sig"
)

print(f"✅ 已儲存原始資料: {raw_filename}")

# =========================================
# Heatmap
# =========================================

generate_foreign_buy_top30(
    df,
    today_str
)

# =========================================
# Cleanup
# =========================================

cleanup_old_data()

print("\n🎉 main.py 執行完成")
