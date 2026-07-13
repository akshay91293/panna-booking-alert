import config
import fetcher
import parser
import comparer
import notifier
import scoring
import state


def run():

    print("Downloading page...")

    html = fetcher.download(config.URL)

    snapshot = parser.parse(html)

    current = snapshot.to_dict()

    previous = state.load_state()

    if not previous:

        print("First run detected.")

        state.save_state(current)

        return

    changes = comparer.compare(previous, current)

    if not changes:

        print("No changes detected.")

        return

    score, scored = scoring.calculate(changes)

    lines = []

    lines.append(f"🐯 {config.PARK_NAME}")
    lines.append("")
    lines.append(scoring.level(score))
    lines.append("")
    lines.append(f"Confidence Score: {score}")
    lines.append("")
    lines.append("Detected changes:")
    lines.append("")

    for item in scored:

        c = item["change"]

        lines.append(
            f"• {item['label']} (+{item['weight']})"
        )

        lines.append(f"Previous: {c.previous}")

        lines.append(f"Current : {c.current}")

        lines.append("")

    if score >= 8:

        lines.append("🚨 Recommendation")

        lines.append(
            "Open the MP Forest booking portal immediately."
        )

    elif score >= 5:

        lines.append("⚠ Recommendation")

        lines.append(
            "Keep a close watch on the booking portal."
        )

    else:

        lines.append("ℹ Recommendation")

        lines.append(
            "Likely a routine website update."
        )

    message = "\n".join(lines)

    print(message)

    notifier.send(message)

    state.save_state(current)
