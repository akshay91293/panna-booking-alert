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

    current = parser.get_to_dt(response.text)

    saved = state.load_state()

    previous = saved.get("to_dt")

    print()
    print("Previous :", previous)
    print("Current  :", current)
    print()

    # First run
    if previous is None:

        print("First run detected.")
        print("Saving current value.")

        saved["to_dt"] = current

        state.save_state(saved)

        return

    # Something changed
    if previous != current:

        message = f"""
🐯 {config.PARK_NAME}

🚨 CHANGE DETECTED!

Previous

{previous}

Current

{current}

Check the MP Forest website immediately.
"""

        print(message)

        notifier.send(message)

        saved["to_dt"] = current

        state.save_state(saved)

        return

    # Nothing changed
    print("No change detected.")
