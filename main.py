print("🚀 main.py 啟動")

print("📦 import fetch_twse")
from modules.fetch_twse import fetch_twse_data

print("📦 import validation")
from modules.validation import run_validation

print("📦 import accumulation")
from modules.accumulation import analyze_foreign_accumulation

print("📦 import cleanup")
from modules.cleanup import cleanup_old_files

print("✅ 所有 import 完成")


def main():

    print("🚀 開始執行 main()")

    csv_path = fetch_twse_data()

    if csv_path is None:

        print("❌ 今日無資料")

        return

    print("📥 開始驗證資料")

    run_validation(csv_path)

    analyze_foreign_accumulation(
        lookback_days=10,
        min_buy_days=8
    )

    cleanup_old_files(days=20)

    print("🎉 main.py 執行完成")


if __name__ == "__main__":

    main()
