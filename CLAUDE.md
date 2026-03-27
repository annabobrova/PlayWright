# PlayWright Study Project

## Commands

### Setup
```bash
pip install -r requirements.txt && playwright install
```

### Running Tests
```bash
# All tests
pytest

# Specific suite
pytest tests/APIs/
pytest tests/UItests/

# Single file
pytest tests/UItests/test_RegisterUser.py

# Single function
pytest tests/UItests/test_RegisterUser.py::test_example

# With HTML report
pytest --html=report.html

# Headless mode
pytest --headless=true

# With slow motion (ms)
pytest --playwright-slowmo=500
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
