import requests


def send_line_message(
    token,
    user_id,
    message
):

    url = (
        "https://api.line.me/"
        "v2/bot/message/push"
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

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print(
            "LINE response:",
            response.status_code
        )

        print(response.text)

    except Exception as e:

        print("❌ LINE發送失敗")

        print(e)
