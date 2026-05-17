# modules/cleanup.py

from pathlib import Path
import shutil


KEEP_FILES = 20


def cleanup_old_files():

    print("🧹 開始資料清理")

    data_dir = Path("data")
    archive_dir = Path("archive")

    archive_dir.mkdir(exist_ok=True)

    csv_files = sorted(data_dir.glob("*.csv"))

    # 保留最近20個
    if len(csv_files) <= KEEP_FILES:
        print("✅ 無需清理")
        return

    old_files = csv_files[:-KEEP_FILES]

    for file in old_files:

        target = archive_dir / file.name

        shutil.move(str(file), str(target))

        print(f"📦 已封存: {file.name}")

    print("✅ cleanup完成")
