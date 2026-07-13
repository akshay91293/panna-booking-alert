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

    changes = comparer.compare(previous, current)

    print(f"Detected {len(changes)} HTML changes.")

    import browser

    print("Launching browser...")

    result = browser.verify()

    print(result)

    if changes:
        notifier.send("HTML changed!")

    state.save_state(current)

    state.save_state(current)
