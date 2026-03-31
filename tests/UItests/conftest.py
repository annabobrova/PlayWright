import os
import sys
import re
import pytest
from typing import Generator
from playwright.sync_api import Browser, Page, expect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from config import BASE_URL, LOGIN_EMAIL, LOGIN_PASSWORD

AUTH_STATE_PATH = "auth/state.json"


def _is_auth_state_valid(browser: Browser) -> bool:
    """
    Checks if the saved auth state is still valid by loading it into a
    temporary context and verifying the header shows 'Logged in as'.
    """
    context = browser.new_context(storage_state=AUTH_STATE_PATH)
    page = context.new_page()
    page.goto(BASE_URL)
    is_valid = page.locator("#header").filter(has_text="Logged in as").count() > 0
    context.close()
    return is_valid


def _do_login(browser: Browser) -> None:
    """
    Performs a fresh login via the UI and saves the session to auth/state.json.
    """
    context = browser.new_context()
    page = context.new_page()

    page.goto(BASE_URL)
    page.get_by_role("link", name=" Signup / Login").click()
    page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(LOGIN_EMAIL)
    page.get_by_role("textbox", name="Password").fill(LOGIN_PASSWORD)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#header")).to_contain_text("Logged in as")

    os.makedirs("auth", exist_ok=True)
    context.storage_state(path=AUTH_STATE_PATH)
    context.close()


@pytest.fixture
def auth_state(browser: Browser) -> str:
    """
    Returns the path to a valid auth state file.
    Reuses the saved file if it exists and the session is still active.
    Triggers a fresh login if the file is missing or the session has expired.
    """
    if os.path.exists(AUTH_STATE_PATH) and _is_auth_state_valid(browser):
        return AUTH_STATE_PATH

    _do_login(browser)
    return AUTH_STATE_PATH


@pytest.fixture
def logged_in_page(browser: Browser, auth_state: str, request) -> Generator[Page, None, None]:
    """
    Creates a browser context pre-loaded with the saved auth state.
    Each test gets a fresh context — no login UI needed.
    """
    context = browser.new_context(storage_state=auth_state)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    ad_regex = re.compile(r"googleads|doubleclick|quantserve|facebook")
    page.route(ad_regex, lambda route: route.abort())

    page.goto(BASE_URL)

    yield page

    os.makedirs("traces", exist_ok=True)
    context.tracing.stop(path=f"traces/trace-{request.node.name}.zip")
    context.close()
