from playwright.sync_api import sync_playwright
import config

URL = config.URL


def verify():

    results = []

    last_dialog = {"text": None}

    def handle_dialog(dialog):
        last_dialog["text"] = dialog.message
        print("ALERT:", dialog.message)
        dialog.accept()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1600, "height": 900}
        )

        page.on("dialog", handle_dialog)

        for safari_date in config.TARGET_DATES:

            print(f"Checking {safari_date['label']}")

            last_dialog["text"] = None

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

            if last_dialog["text"]:

                if "Park Closed" in last_dialog["text"]:
                    status = "PARK_CLOSED"
                else:
                    status = "ALERT"

            else:
                status = "POSSIBLY_OPEN"

            result = {
                "date": safari_date["label"],
                "status": status,
                "alert": last_dialog["text"]
            }

            print(result)

            results.append(result)

        page.screenshot(
            path="booking_attempt.png",
            full_page=True
        )

        browser.close()

    return results
