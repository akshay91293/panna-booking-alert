import os
import requests
from bs4 import BeautifulSoup

URL = "https://forest.mponline.gov.in/Search.aspx?park=3"
EXPECTED_TO_DT = "9/30/2026 11:59:59 PM"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram secrets not configured.")
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=30,
    )


print("Downloading page...")

response = requests.get(URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

to_dt = soup.find(id="To_dt")

if not to_dt:
    raise Exception("Could not find To_dt field")

current = to_dt["value"]

print("Expected:", EXPECTED_TO_DT)
print("Current :", current)

if current != EXPECTED_TO_DT:

    message = f"""🐯 Panna Booking Monitor

CHANGE DETECTED!

Expected:
{EXPECTED_TO_DT}

Current:
{current}

Check the MP Forest website immediately.
"""

    print(message)

    send_telegram(message)

else:

    print("No change detected.")

    send_telegram(
        f"""✅ Panna Monitor Test

Everything is working.

Current backend date:

{current}

No change detected."""
    )
