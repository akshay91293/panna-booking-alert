from playwright.sync_api import sync_playwright


URL = "https://forest.mponline.gov.in/Search.aspx?park=3"


def verify():

    result = {
        "status": "unknown",
        "alert": None
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1600, "height": 900}
        )

        # Capture javascript alerts
        def handle_dialog(dialog):
            print("ALERT:", dialog.message)
            result["alert"] = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)

        page.goto(URL, wait_until="networkidle")

        print("Title:", page.title())

        # Select Full Vehicle
        page.check("#rdFullVehicle")

        print("Selected Full Vehicle")

        # Fill the date directly
        page.evaluate("""
            () => {
                document.querySelector('#txtdate').value =
                    'Thu, 15 October 2026';
            }
        """)

        print("Date entered")

        # Click Search
        page.click("#btnshow")

        # Wait a few seconds for postback / alert
        page.wait_for_timeout(5000)

        page.screenshot(
            path="booking_attempt.png",
            full_page=True
        )

        browser.close()

    if result["alert"]:

        result["status"] = "closed"

    else:

        result["status"] = "unknown"

    return result
