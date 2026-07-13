from playwright.sync_api import sync_playwright
import config

URL = config.URL


def check_date(page, safari_date):

    result = {
        "date": safari_date["label"],
        "status": "UNKNOWN",
        "alert": None
    }

    dialog_message = {"text": None}

    def handle_dialog(dialog):
        dialog_message["text"] = dialog.message
        dialog.accept()

    page.remove_listener("dialog", handle_dialog)
    page.on("dialog", handle_dialog)

    page.goto(URL, wait_until="networkidle")

    page.check("#rdFullVehicle")

    page.evaluate(
        """(value) => {
            document.querySelector("#txtdate").value = value;
        }""",
        safari_date["date"]
    )

    page.click("#btnshow")

    page.wait_for_timeout(3000)

    if dialog_message["text"]:

        result["alert"] = dialog_message["text"]

        if "Park Closed" in dialog_message["text"]:
            result["status"] = "PARK_CLOSED"

        else:
            result["status"] = "ALERT"

    else:

        result["status"] = "POSSIBLY_OPEN"

    return result


def verify():

    output = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1600,
                "height": 900
            }
        )

        for safari_date in config.TARGET_DATES:

            print(f"Checking {safari_date['label']}")

            result = check_date(page, safari_date)

            print(result)

            output.append(result)

        page.screenshot(
            path="booking_attempt.png",
            full_page=True
        )

        browser.close()

    return output
