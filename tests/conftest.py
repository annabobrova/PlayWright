import os, re
import sys
from typing import Any, Generator # Import Generator and Any for type hinting

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default="false", help="run tests in headless mode (true/false)")
    parser.addoption("--playwright-slowmo", action="store", default="0", help="slow down Playwright actions (milliseconds)")

def pytest_configure(config):
    # This hook runs after command line options have been parsed
    # Insert project root to sys.path to allow imports like 'from pages.homepage import HomePage'
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def browser(request) -> Generator[Browser, Any, None]:
    headless = request.config.getoption("--headless").lower() == "true"
    slow_mo = int(request.config.getoption("--playwright-slowmo"))
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def context(browser: Browser, request) -> Generator[BrowserContext, Any, None]: # Corrected type hint
    context = browser.new_context()
    # start tracing for the test: screenshots, DOM snapshots and source files
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    try:
        yield context
    finally:
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
    Optimized ad blocker that only intercepts specific ad domains
    without interfering with other API calls.
    """
    # Use a regex to target ONLY ads, leaving other traffic alone
    ad_regex = re.compile(r"googleads|doubleclick|quantserve|facebook")
    
    # We only route requests that match the ad pattern
    page.route(ad_regex, lambda route: route.abort())

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the Pytest HTML Report to include a screenshot if a test fails.
    Also adds the test docstring as a Description entry in the report.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        report.description = (item.function.__doc__ or "").strip()

    if report.when == "call" and report.failed:
        # Get the 'page' fixture from the test item
        page = item.funcargs.get("page")
        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.nodeid.replace('::', '_').replace('/', '_')}.png"
            page.screenshot(path=screenshot_path)
            if pytest_html is not None:
                # Add the screenshot to the HTML report
                extras.append(pytest_html.extras.image(screenshot_path))
    
    report.extras = extras


def pytest_html_results_table_header(cells):
    cells.insert(2, "Description")


def pytest_html_results_table_row(report, cells):
    description = getattr(report, "description", "")
    cells.insert(2, description)
