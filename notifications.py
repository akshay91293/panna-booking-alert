from datetime import datetime
from zoneinfo import ZoneInfo

import config
import notifier
import scoring


def process(previous, current, html_changes, browser_results):

    previous_browser = previous.get("browser_results", {})
    current_browser = {}

    booking_changed = False
    booking_lines = []

    for result in browser_results:

        current_browser[result["date"]] = result["status"]

        old = previous_browser.get(result["date"])
        new = result["status"]

        if old != new:
            booking_changed = True

        icon = "❌"

        if new == "POSSIBLY_OPEN":
            icon = "✅"

        elif new == "UNKNOWN":
            icon = "❓"

        booking_lines.append(
            f"{icon} {result['date']}  {config.STATUS_TEXT.get(new,new)}"
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

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    today = now.date().isoformat()

    daily_health = (

        now.hour == config.DAILY_HEALTH_REPORT_HOUR

        and

        previous.get("health_report_date") != today

    )

    #
    # Booking Alert
    #

    if booking_changed:

        msg = []

        msg.append("🐯 Panna Monitor")
        msg.append("")
        msg.append("🚨 Booking Status Changed")
        msg.append("")
        msg.append("Booking Status")
        msg.append("")
        msg.extend(booking_lines)

        msg.append("")
        msg.append("────────────────────")
        msg.append("")
        msg.append(
            f"Run Time\n{now.strftime('%d %b %Y %H:%M IST')}"
        )

        notifier.send_photo(
            "booking_attempt.png",
            "\n".join(msg)
        )

        return

    #
    # Important Website Update
    #

    if important:

        msg = []

        msg.append("🐯 Panna Monitor")
        msg.append("")
        msg.append("🚨 Website Updated")
        msg.append("")

        for item in important:

            msg.append(
                f"• {item}"
            )

        msg.append("")
        msg.append("────────────────────")
        msg.append("")
        msg.append(
            f"Run Time\n{now.strftime('%d %b %Y %H:%M IST')}"
        )

        notifier.send(
            "\n".join(msg)
        )

        return

    #
    # Daily Health Report
    #

    if daily_health:

        msg = []

        msg.append("🐯 Panna Monitor")
        msg.append("")
        msg.append("✅ Monitor is healthy")
        msg.append("")
        msg.append(
            f"🕒 Last checked\n{now.strftime('%d %b %Y %H:%M IST')}"
        )

        msg.append("")
        msg.append("────────────────────")
        msg.append("")
        msg.append("Booking Status")
        msg.append("")
        msg.extend(booking_lines)

        msg.append("")
        msg.append("────────────────────")
        msg.append("")
        msg.append("Website")
        msg.append("")

        if informational:

            for item in informational:

                msg.append(
                    f"• {item}"
                )

        else:

            msg.append(
                "No significant changes detected."
            )

        msg.append("")
        msg.append("🌿 Still keeping watch...")

        notifier.send(
            "\n".join(msg)
        )

        current["health_report_date"] = today

        return

    print("No meaningful changes.")
