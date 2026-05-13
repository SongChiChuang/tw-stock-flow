import os
import glob


def cleanup_old_files(keep=5):

    print("🧹 開始資料清理")

    data_dir = "data"

    csv_files = sorted(
        glob.glob(os.path.join(data_dir, "*.csv"))
    )

    if len(csv_files) <= keep:

        print(f"✅ cleanup完成（封存 0 個檔案）")
        return

    remove_files = csv_files[:-keep]

    archive_dir = "archive"

    os.makedirs(archive_dir, exist_ok=True)

    for file in remove_files:

        filename = os.path.basename(file)

        target = os.path.join(
            archive_dir,
            filename
        )

        os.rename(file, target)

        print(f"📦 已封存: {filename}")

    print(f"✅ cleanup完成（封存 {len(remove_files)} 個檔案）")
