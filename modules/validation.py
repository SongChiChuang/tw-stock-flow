import os
import re
import sys

import pandas as pd

# =========================================
# Validation Report
# =========================================

validation_logs = []

def add_pass(msg):

    validation_logs.append(f"[PASS] {msg}")

    print(f"✅ {msg}")

def add_warning(msg):

    validation_logs.append(f"[WARNING] {msg}")

    print(f"⚠️ WARNING: {msg}")

def add_fail(msg):

    validation_logs.append(f"[FAIL] {msg}")

    print(f"❌ FAIL: {msg}")

    save_validation_report()

    sys.exit(1)

# =========================================
# 儲存 validation report
# =========================================

def save_validation_report(today_str=None):

    os.makedirs(
        "reports/validation",
        exist_ok=True
    )

    if today_str is None:

        filename = "latest_validation.txt"

    else:

        filename = f"{today_str}_validation.txt"

    report_path = (
        f"reports/validation/{filename}"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(validation_logs))

# =========================================
# 主驗證函式
# =========================================

def validate_dataframe(df, today_str=None):

    # =====================================
    # 欄位名稱清理
    # =====================================

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # =====================================
    # 必要欄位驗證
    # =====================================

    required_columns = [

        "證券代號",
        "證券名稱",
        "外陸資買賣超股數(不含外資自營商)",
        "投信買賣超股數"

    ]

    for col in required_columns:

        if col not in df.columns:

            add_fail(f"缺少必要欄位: {col}")

    add_pass("必要欄位完整")

    # =====================================
    # row count validation
    # =====================================

    row_count = len(df)

    if row_count < 1000:

        add_fail(f"股票數量異常: {row_count}")

    add_pass(f"股票數量正常: {row_count}")

    # =====================================
    # 股票代號格式驗證
    # =====================================

    stock_pattern = re.compile(
        r"^[0-9A-Z]{4,6}$"
    )

    invalid_codes = []

    for code in df["證券代號"]:

        if not stock_pattern.match(
            str(code)
        ):

            invalid_codes.append(code)

    if len(invalid_codes) > 0:

        add_warning(
            f"發現異常股票代號: "
            f"{invalid_codes[:10]}"
        )

    else:

        add_pass("股票代號格式正常")

    # =====================================
    # duplicate驗證
    # =====================================

    duplicate_codes = df[
        df["證券代號"].duplicated()
    ]

    if len(duplicate_codes) > 0:

        add_fail("發現重複股票代號")

    add_pass("無重複股票代號")

    # =====================================
    # 數值欄位
    # =====================================

    numeric_columns = [

        col for col in df.columns

        if any(keyword in col for keyword in [

            "買進股數",
            "賣出股數",
            "買賣超股數"

        ])
    ]

    for col in numeric_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
            .replace("", "0")
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    add_pass("數值欄位轉換完成")

    # =====================================
    # 異常值 Warning
    # =====================================

    warning_threshold = 300000000

    foreign_col = (
        "外陸資買賣超股數(不含外資自營商)"
    )

    abnormal_df = df[
        abs(df[foreign_col])
        > warning_threshold
    ]

    if len(abnormal_df) > 0:

        add_warning(
            f"發現異常大買賣超股票數量: "
            f"{len(abnormal_df)}"
        )

    else:

        add_pass("未發現異常大買賣超")

    # =====================================
    # 歷史row count比較
    # =====================================

    history_files = sorted(
        os.listdir("data")
    ) if os.path.exists("data") else []

    if len(history_files) >= 1:

        latest_file = history_files[-1]

        try:

            old_df = pd.read_csv(
                f"data/{latest_file}"
            )

            old_count = len(old_df)

            diff_ratio = abs(
                row_count - old_count
            ) / old_count

            if diff_ratio > 0.2:

                add_warning(
                    f"股票數量較前次變動超過20% "
                    f"(舊:{old_count} 新:{row_count})"
                )

            else:

                add_pass("股票數量波動正常")

        except:

            add_warning("歷史資料比較失敗")

    # =====================================
    # 儲存 validation report
    # =====================================

    save_validation_report(today_str)

    print("\n===================")
    print("Validation 完成")
    print("===================")

    return df
