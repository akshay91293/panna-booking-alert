from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        viewport={"width": 1600, "height": 900}
    )

    page.goto(
        "https://forest.mponline.gov.in/Search.aspx?park=3",
        wait_until="networkidle"
    )

    page.screenshot(path="screenshot.png", full_page=True)

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    browser.close()
