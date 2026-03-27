"""
Run this to print all links and buttons on the numerical test page.
Usage: python3 tests/PracticeAptitude/debug_selectors.py
"""
from playwright.sync_api import sync_playwright

AUTH_FILE = "tests/PracticeAptitude/auth.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()

    page.goto("https://www.practiceaptitudetests.com/numerical-reasoning-tests/")
    page.wait_for_load_state("networkidle")

    print("\n=== LINKS ===")
    links = page.locator("a").all()
    for link in links:
        print(repr(link.inner_text().strip()), "->", link.get_attribute("href"))

    print("\n=== BUTTONS ===")
    buttons = page.locator("button").all()
    for button in buttons:
        print(repr(button.inner_text().strip()))

    browser.close()
