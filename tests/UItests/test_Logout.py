import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage


@pytest.mark.ui
def test_logout(logged_in_page: Page) -> None:
    """
    Verify that a logged-in user can log out successfully.
    """
    home_page = HomePage(logged_in_page)

    # Verify user is logged in
    expect(logged_in_page.locator("#header")).to_contain_text("Logged in as")

    # Click Logout
    home_page.logout()

    # Verify user is logged out
    expect(logged_in_page.get_by_role("link", name=" Signup / Login")).to_be_visible()
    expect(logged_in_page.locator("#header")).not_to_contain_text("Logged in as")
