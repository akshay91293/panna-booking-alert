import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send(message: str):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    response.raise_for_status()


def send_photo(photo_path: str, caption: str = ""):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={
                "photo": photo
            },
            timeout=60
        )

    response.raise_for_status()
