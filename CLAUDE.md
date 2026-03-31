# PlayWright Study Project

## Commands

### Setup
```bash
pip install -r requirements.txt && playwright install
```

### Running Tests
```bash
# All tests
python3 -m pytest

# Specific suite
python3 -m pytest tests/APIs/
python3 -m pytest tests/UItests/

# Single file
python3 -m pytest tests/UItests/test_RegisterUser.py

# Single function
python3 -m pytest tests/UItests/test_RegisterUser.py::test_example

# With HTML report
python3 -m pytest --html=report.html

# Headless mode
python3 -m pytest --headless=true

# With slow motion (ms)
python3 -m pytest --playwright-slowmo=500
```

### Debugging
```bash
# View Playwright trace
playwright show-trace traces/<trace-file>.zip
```

## Architecture

Two test suites targeting https://automationexercise.com:

- **`tests/UItests/`** — Browser UI tests using the Page Object Model (`pages/` directory)
- **`tests/APIs/`** — API tests using Playwright's built-in `page.request` HTTP client (not the `requests` library)

### Shared infrastructure
- **`conftest.py`** — Session-scoped browser fixture, per-test context with tracing enabled, ad-blocking
- **`config.py`** — Shared configuration (base URLs, credentials, etc.)
- **`utils.py`** — Shared helper utilities

### Page Object Model
Used only in `tests/UItests/`. Each page has a corresponding class in `pages/` that encapsulates selectors and actions.

### API Testing
API tests use `page.request` (Playwright's built-in HTTP client) rather than the `requests` library, keeping API and UI tests in the same Playwright context.

## Selector conventions

Always prefer Playwright's semantic Locator API over raw CSS/XPath strings. Use in this order of preference:

1. `get_by_role()` — for interactive elements (buttons, links, inputs, checkboxes, etc.)
2. `get_by_label()` — for form fields with an associated `<label>`
3. `get_by_placeholder()` — for inputs/textareas with placeholder text
4. `get_by_text()` — for non-interactive elements identified by visible text
5. `get_by_title()` / `get_by_alt_text()` — for elements with title or alt attributes
6. CSS/attribute selectors (`locator("...")`) — only when no semantic locator applies (e.g., structural layout containers like `.features_items`, or `<select>` elements without accessible labels)
