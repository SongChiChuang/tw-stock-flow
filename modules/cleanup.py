import os
import shutil
import zipfile

from datetime import datetime

# =========================================
# 設定
# =========================================

DATA_FOLDER = "data"

ARCHIVE_FOLDER = "archive"

KEEP_DAYS = 30

# =========================================
# cleanup function
# =========================================

def cleanup_old_data():

    print("\n🧹 開始資料清理")

    # 建立 archive 資料夾

    os.makedirs(
        ARCHIVE_FOLDER,
        exist_ok=True
    )

    # 取得 data 內所有 csv

    files = [

        f for f in os.listdir(DATA_FOLDER)

        if f.endswith(".csv")
    ]

    now = datetime.now()

    moved_count = 0

    for file in files:

        try:

            # 解析日期

            date_str = file.replace(".csv", "")

            file_date = datetime.strptime(
                date_str,
                "%Y%m%d"
            )

            diff_days = (
                now - file_date
            ).days

            # 超過 KEEP_DAYS

            if diff_days > KEEP_DAYS:

                src_path = (
                    f"{DATA_FOLDER}/{file}"
                )

                # zip名稱

                zip_name = (
                    f"{date_str}.zip"
                )

                zip_path = (
                    f"{ARCHIVE_FOLDER}/{zip_name}"
                )

                # 建立zip

                with zipfile.ZipFile(
                    zip_path,
                    "w",
                    zipfile.ZIP_DEFLATED
                ) as zipf:

                    zipf.write(
                        src_path,
                        arcname=file
                    )

                # 刪除原csv

                os.remove(src_path)

                moved_count += 1

                print(
                    f"📦 已封存: {file}"
                )

        except Exception as e:

            print(
                f"⚠️ cleanup失敗: {file}"
            )

            print(e)

    print(
        f"\n✅ cleanup完成 "
        f"(封存 {moved_count} 個檔案)"
    )
