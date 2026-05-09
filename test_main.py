import pandas as pd

from modules.validation import validate_dataframe

# =========================================
# 測試資料路徑
# =========================================

TEST_FILE = "data/20260509.csv"

# =========================================
# 讀取測試資料
# =========================================

print(f"\n📂 讀取測試資料: {TEST_FILE}")

df = pd.read_csv(
    TEST_FILE,
    dtype=str
)

print("✅ 測試資料讀取成功")

# =========================================
# 執行 validation
# =========================================

df = validate_dataframe(
    df,
    today_str="TEST"
)

print("\n🎉 test_main.py 執行完成")
