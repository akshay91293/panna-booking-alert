import browser
import comparer
import config
import fetcher
import notifications
import parser
import state


def run():

    print("Downloading page...")

    html = fetcher.download(config.URL)

    snapshot = parser.parse(html)

    current = snapshot.to_dict()

    previous = state.load_state()

    #
    # Compare website only
    #

    previous_compare = previous.copy()
    current_compare = current.copy()

    previous_compare.pop("browser_results", None)
    current_compare.pop("browser_results", None)

    previous_compare.pop("health_report_date", None)
    current_compare.pop("health_report_date", None)

    html_changes = comparer.compare(
        previous_compare,
        current_compare
    )

    #
    # Browser Verification
    #

    browser_results = browser.verify()

    #
    # Notifications
    #

    notifications.process(
        previous,
        current,
        html_changes,
        browser_results
    )

    #
    # Persist latest state
    #

    state.save_state(current)
