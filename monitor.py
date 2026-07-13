import requests

import config
import notifier
import parser


def run():

    print("Downloading page...")

    response = requests.get(
        config.URL,
        timeout=30
    )

    response.raise_for_status()

    current = parser.get_to_dt(response.text)

    print()

    print("Expected :", config.EXPECTED_TO_DT)
    print("Current  :", current)

    print()

    if current != config.EXPECTED_TO_DT:

        message = f"""
🐯 {config.PARK_NAME}

CHANGE DETECTED

Expected

{config.EXPECTED_TO_DT}

Current

{current}

Check booking immediately.
"""

        print(message)

        notifier.send(message)

    else:

        print("No change detected.")

        notifier.send(
f"""✅ {config.PARK_NAME}

Everything is working.

Current backend date

{current}

No change detected."""
)
