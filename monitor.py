import config
import fetcher
import parser
import comparer
import notifier
import state


def run():

    print("Downloading page...")

    html = fetcher.download(config.URL)

    current = parser.parse(html)

    previous = state.load_state()

    if not previous:

        print("First run detected.")

        state.save_state(current)

        return

    changes = comparer.compare(previous, current)

    if not changes:

        print("No changes detected.")

        return

    lines = []

    lines.append(f"🐯 {config.PARK_NAME}")
    lines.append("")
    lines.append("Changes detected:")
    lines.append("")

    for item in changes:

        lines.append(f"• {item['field']}")
        lines.append(f"Previous: {item['previous']}")
        lines.append(f"Current : {item['current']}")
        lines.append("")

    message = "\n".join(lines)

    print(message)

    notifier.send(message)

    state.save_state(current)
