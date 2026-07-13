import browser
import comparer
import config
import fetcher
import notifier
import parser
import scoring
import state

from datetime import datetime
from zoneinfo import ZoneInfo


def run():

    print("Downloading page...")

    html = fetcher.download(config.URL)

    snapshot = parser.parse(html)
    current = snapshot.to_dict()

    previous = state.load_state()

    previous_compare = previous.copy()
    current_compare = current.copy()

    previous_compare.pop("browser_results", None)
    current_compare.pop("browser_results", None)
    previous_compare.pop("health_report_date", None)
    current_compare.pop("health_report_date", None)

    html_changes = comparer.compare(previous_compare, current_compare)

    browser_results = browser.verify()

    previous_browser = previous.get("browser_results", {})
    current_browser = {}

    booking_changed = False
    booking_lines = []

    for result in browser_results:

        current_browser[result["date"]] = result["status"]

        if previous_browser.get(result["date"]) != result["status"]:
            booking_changed = True

        icon = "❌"
        if result["status"] == "POSSIBLY_OPEN":
            icon = "✅"
        elif result["status"] == "UNKNOWN":
            icon = "❓"

        booking_lines.append(
            f'{icon} {result["date"]}  {config.STATUS_TEXT.get(result["status"], result["status"])}'
        )

    current["browser_results"] = current_browser

    score, scored = scoring.calculate(html_changes)

    important = []
    informational = []

    for item in scored:
        if item["field"] in config.IMPORTANT_FIELDS:
            important.append(item["label"])
        elif item["field"] in config.INFO_FIELDS:
            informational.append(item["label"])

    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    today = now.date().isoformat()

    daily_health = (
        now.hour == config.DAILY_HEALTH_REPORT_HOUR
        and previous.get("health_report_date") != today
    )

    if booking_changed:

        msg = [
            "🐯 Panna Monitor",
            "",
            "🚨 Booking Status Changed",
            "",
            "Booking Status",
            ""
        ]
        msg.extend(booking_lines)

        notifier.send_photo("booking_attempt.png", "\n".join(msg))

    elif important:

        msg = [
            "🐯 Panna Monitor",
            "",
            "🚨 Website Updated",
            ""
        ]

        for x in important:
            msg.append(f"• {x}")

        notifier.send("\n".join(msg))

    elif daily_health:

        msg = [
            "🐯 Panna Monitor",
            "",
            "✅ Monitor is healthy",
            "",
            f"🕒 Last checked\n{now.strftime('%d %b %Y %H:%M IST')}",
            "",
            "──────────────",
            "",
            "Booking Status",
            ""
        ]

        msg.extend(booking_lines)

        msg.extend([
            "",
            "──────────────",
            "",
            "Website"
        ])

        if informational:
            for x in informational:
                msg.append(f"• {x}")
        else:
            msg.append("No significant changes detected.")

        msg.extend([
            "",
            "🌿 Still keeping watch..."
        ])

        notifier.send("\n".join(msg))
        current["health_report_date"] = today

    else:
        print("No meaningful changes.")

    state.save_state(current)
