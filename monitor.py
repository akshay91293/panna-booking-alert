import browser
import comparer
import config
import fetcher
import notifier
import parser
import scoring
import state


def run():

    print("Downloading page...")

    html = fetcher.download(config.URL)

    snapshot = parser.parse(html)

    current = snapshot.to_dict()

    previous = state.load_state()

    html_changes = comparer.compare(previous, current)

    browser_results = browser.verify()

    print()

    print("Browser Results")

    print(browser_results)

    message = []

    message.append(f"🐯 {config.PARK_NAME}")

    message.append("")

    message.append("Booking Status")

    message.append("")

    notify = False

    previous_browser = previous.get(
        "browser_results",
        {}
    )

    current_browser = {}

    for result in browser_results:

        current_browser[result["date"]] = result["status"]

        old = previous_browser.get(result["date"])

        new = result["status"]

        if old != new:

            notify = True

        icon = "✅"

        if new == "PARK_CLOSED":
            icon = "❌"

        elif new == "UNKNOWN":
            icon = "❓"

        message.append(
            f"{icon} {result['date']} : {new}"
        )

    current["browser_results"] = current_browser

    state.save_state(current)

    if notify:

        caption = "\n".join(message)

        notifier.send_photo(
            "booking_attempt.png",
            caption
        )

        notifier.send(caption)

    elif html_changes:

        score, scored = scoring.calculate(html_changes)

        lines = []

        lines.append(f"🐯 {config.PARK_NAME}")

        lines.append("")

        lines.append("Website updated")

        lines.append("")

        for item in scored:

            lines.append(
                f"• {item['label']}"
            )

        notifier.send(
            "\n".join(lines)
        )

    else:

        print("No meaningful changes.")
