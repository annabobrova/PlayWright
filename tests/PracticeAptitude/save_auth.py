"""
Run this script once to save your Google auth session.
It opens a real browser - log in manually, then close the browser.
The session is saved to auth.json and reused by tests.

Usage: python3 tests/PracticeAptitude/save_auth.py
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.practiceaptitudetests.com/sign-in")

    print("Log in with Google in the browser window.")
    print("Once you are on the dashboard, press Enter here to save the session.")
    input()

    context.storage_state(path="tests/PracticeAptitude/auth.json")
    print("Session saved to tests/PracticeAptitude/auth.json")
    browser.close()
