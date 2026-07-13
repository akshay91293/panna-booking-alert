import requests

import config
import notifier
import parser
import state


def run():

    print("Downloading page...")

    response = requests.get(
        config.URL,
        timeout=30
    )

    response.raise_for_status()

    current = parser.parse(response.text)

    previous = state.load_state()

    if not previous:

        print("First run detected.")

        state.save_state(current)

        return

    changes = []

    for key in current:

        if previous.get(key) != current.get(key):

            changes.append(key)

    if not changes:

        print("No changes detected.")

        return

    message = f"🐯 {config.PARK_NAME}\n\n"

    message += "Changes detected:\n\n"

    for key in changes:

        message += (
            f"• {key}\n"
            f"Previous: {previous.get(key)}\n"
            f"Current : {current.get(key)}\n\n"
        )

    print(message)

    notifier.send(message)

    state.save_state(current)
