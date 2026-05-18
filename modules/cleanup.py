# modules/cleanup.py

from pathlib import Path
from datetime import datetime


def cleanup_old_files(days=20):

    print(f"🧹 開始清理 {days} 天前資料")

    data_dir = Path("data")

    if not data_dir.exists():

        print("⚠️ data資料夾不存在")

        return

    csv_files = sorted(
        data_dir.glob("*.csv")
    )

    if len(csv_files) <= days:

        print("✅ 無需清理")

        return

    old_files = csv_files[:-days]

    for file in old_files:

        try:

            file.unlink()

            print(f"🗑️ 已刪除: {file.name}")

        except Exception as e:

            print(f"❌ 刪除失敗 {file.name}: {e}")

    print("✅ 清理完成")
