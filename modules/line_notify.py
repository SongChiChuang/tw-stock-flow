import requests


def send_line_message(
    token,
    user_id,
    message
):

    try:

        if not token:

            print("❌ LINE token不存在")

            return

        if not user_id:

            print("❌ LINE user_id不存在")

            return

        url = (
            "https://api.line.me/v2/bot/message/push"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(
            f"📨 LINE status: "
            f"{response.status_code}"
        )

        print(response.text)

        if response.status_code == 200:

            print("✅ LINE通知成功")

        else:

            print("❌ LINE通知失敗")

    except Exception as e:

        print("❌ LINE發送異常")

        print(e)
