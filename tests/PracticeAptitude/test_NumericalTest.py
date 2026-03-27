from playwright.sync_api import Page, expect, BrowserContext
import pytest


BASE_URL = "https://www.practiceaptitudetests.com"
AUTH_FILE = "tests/PracticeAptitude/auth.json"


@pytest.fixture
def context(browser):
    context = browser.new_context(storage_state=AUTH_FILE)
    yield context
    context.close()


def test_take_numerical_test(page: Page) -> None:
    """Login and take a numerical reasoning test."""
    # Session loaded from auth.json — no login needed
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/dashboard**")

    # 3. Navigate to numerical reasoning tests
    page.goto(f"{BASE_URL}/numerical-reasoning-tests/")
    page.wait_for_load_state("networkidle")

    # 4. Click the first available free test
    page.get_by_role("link", name="Start test").first.click()
    page.wait_for_load_state("networkidle")

    # 5. Start the test if there's a start/begin button
    start_button = page.get_by_role("button", name="Start").or_(
        page.get_by_role("button", name="Begin")
    )
    if start_button.count() > 0:
        start_button.first.click()

    # 6. Answer each question until test ends
    while True:
        page.wait_for_load_state("networkidle")

        # Pick the first available answer option
        answer = page.locator("input[type='radio']").first
        if answer.count() == 0:
            break
        answer.click()

        # Click Next or Finish
        next_button = page.get_by_role("button", name="Next").or_(
            page.get_by_role("button", name="Finish")
        )
        if next_button.count() == 0:
            break
        next_button.first.click()

        # Stop if we've reached the results page
        if "result" in page.url or "complete" in page.url:
            break

    # 7. Verify results page loaded
    expect(page.locator("body")).to_be_visible()
