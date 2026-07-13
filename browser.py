from playwright.sync_api import sync_playwright


def verify():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            "https://forest.mponline.gov.in/Search.aspx?park=3",
            wait_until="networkidle"
        )

        print("Title:", page.title())

        browser.close()

        return {
            "status": "success"
        }
