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

    changes = comparer.compare(previous, current)

    print(f"Detected {len(changes)} HTML changes.")

    print("Launching browser...")

    result = browser.verify()

    print(result)

    if changes:

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

            lines.append(f"• {item['label']} (+{item['weight']})")
            lines.append(f"Previous: {c.previous}")
            lines.append(f"Current : {c.current}")
            lines.append("")

        notifier.send("\n".join(lines))

    state.save_state(current)
