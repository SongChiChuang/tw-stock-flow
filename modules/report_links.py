import os


def generate_report_links(csv_path):

    file_date = os.path.basename(
        csv_path
    ).replace(".csv", "")

    base_url = (
        "https://songchichuang.github.io/"
        "tw-stock-flow"
    )

    foreign_buy = (
        f"{base_url}/reports/foreign/"
        f"{file_date}_foreign_buy_top30.csv"
    )

    foreign_sell = (
        f"{base_url}/reports/foreign/"
        f"{file_date}_foreign_sell_top30.csv"
    )

    investment_buy = (
        f"{base_url}/reports/investment/"
        f"{file_date}_investment_buy_top30.csv"
    )

    investment_sell = (
        f"{base_url}/reports/investment/"
        f"{file_date}_investment_sell_top30.csv"
    )

    message = (
        "✅ 台股資料更新成功\n\n"

        "📈 外資買超TOP30\n"
        f"{foreign_buy}\n\n"

        "📉 外資賣超TOP30\n"
        f"{foreign_sell}\n\n"

        "🏦 投信買超TOP30\n"
        f"{investment_buy}\n\n"

        "🏦 投信賣超TOP30\n"
        f"{investment_sell}"
    )

    return message
