    def generate_foreign_top30(csv_path):

    print("📊 產生外資 TOP30")

    try:

        df = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        )

        target_col = "外陸資買賣超股數(不含外資自營商)"

        df[target_col] = (
            df[target_col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df[target_col] = pd.to_numeric(
            df[target_col],
            errors="coerce"
        ).fillna(0)

        # =========================
        # 只保留需要欄位
        # =========================

        df = df[[
            "證券代號",
            "證券名稱",
            target_col
        ]]

        # =========================
        # 欄位名稱簡化
        # =========================

        df = df.rename(columns={
            target_col: "外資買賣超股數"
        })

        # =========================
        # 排序
        # =========================

        buy_df = df.sort_values(
            by="外資買賣超股數",
            ascending=False
        ).head(30)

        sell_df = df.sort_values(
            by="外資買賣超股數",
            ascending=True
        ).head(30)

        # =========================
        # 增加排名
        # =========================

        buy_df.insert(
            0,
            "排名",
            range(1, len(buy_df) + 1)
        )

        sell_df.insert(
            0,
            "排名",
            range(1, len(sell_df) + 1)
        )

        os.makedirs(
            "reports/foreign",
            exist_ok=True
        )

        file_date = os.path.basename(
            csv_path
        ).replace(".csv", "")

        buy_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_buy_top30.csv"
        )

        sell_path = (
            f"reports/foreign/"
            f"{file_date}_foreign_sell_top30.csv"
        )

        buy_df.to_csv(
            buy_path,
            index=False,
            encoding="utf-8-sig"
        )

        sell_df.to_csv(
            sell_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"✅ 已輸出: {buy_path}")
        print(f"✅ 已輸出: {sell_path}")

    except Exception as e:

        print("❌ 外資TOP30失敗")

        print(e)
