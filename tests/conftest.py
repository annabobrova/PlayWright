import os
import sys
from typing import Any, Generator # Import Generator and Any for type hinting

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default="false", help="run tests in headless mode (true/false)")

def pytest_configure(config):
    # This hook runs after command line options have been parsed
    # Insert project root to sys.path to allow imports like 'from pages.homepage import HomePage'
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def browser(request) -> Generator[Browser, Any, None]: # Corrected type hint
    headless = request.config.getoption("--headless").lower() == "true"
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless) 
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def context(browser: Browser, request) -> Generator[BrowserContext, Any, None]: # Corrected type hint
    context = browser.new_context()
    # start tracing for the test: screenshots, DOM snapshots and source files
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    # ensure traces directory exists and save trace per-test
    os.makedirs("traces", exist_ok=True)
    trace_path = f"traces/trace-{request.node.name}.zip"
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    return context.new_page()

@pytest.fixture(autouse=True)
def block_ads(page: Page):
    """
    Automatically block ads (googleads, doubleclick) for every test.
    This runs automatically for every test that uses the 'page' fixture.
    """
    page.route("**/*", lambda route: route.abort() 
        if "googleads" in route.request.url or "doubleclick" in route.request.url 
        else route.continue_()
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the Pytest HTML Report to include a screenshot if a test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # Get the 'page' fixture from the test item
        page = item.funcargs.get("page")
        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.nodeid.replace('::', '_').replace('/', '_')}.png"
            page.screenshot(path=screenshot_path)
            if pytest_html is not None:
                # Add the screenshot to the HTML report
                extra.append(pytest_html.extras.image(screenshot_path))
    
    report.extra = extra





