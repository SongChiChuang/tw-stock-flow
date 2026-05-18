# modules/line_notify.py

import os
import requests


def send_line_message(message):

    print("📲 準備發送 LINE 通知")

    token = os.getenv(
        "LINE_CHANNEL_ACCESS_TOKEN"
    )

    user_id = os.getenv(
        "LINE_USER_ID"
    )

    if not token:

        print("❌ 找不到 LINE token")

        return

    if not user_id:

        print("❌ 找不到 LINE user id")

        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
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

    try:

        response = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers=headers,
            json=payload,
            timeout=20
        )

        print("📨 LINE Status:", response.status_code)

        print(response.text)

        if response.status_code == 200:

            print("✅ LINE通知成功")

        else:

            print("❌ LINE通知失敗")

    except Exception as e:

        print("❌ LINE發送錯誤")

        print(e)
