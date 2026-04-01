# Playwright Test Automation Project

A test automation framework built with **Playwright** and **Python**, targeting [AutomationExercise.com](https://automationexercise.com). Covers both UI and API testing using the Page Object Model pattern.

![CI](https://github.com/actions/workflows/playwright.yml/badge.svg)

---

## Tech Stack

- **Python** 3.9+
- **Playwright** — browser automation and HTTP client
- **pytest** — test runner
- **pytest-html** — HTML test reports
- **Docker** — containerized test execution
- **GitHub Actions** — CI/CD pipeline

---

## Project Structure

```
├── pages/              # Page Object Model classes
│   ├── homepage.py
│   ├── signuppage.py
│   ├── productspage.py
│   ├── cartpage.py
│   └── contactuspage.py
├── tests/
│   ├── UItests/        # Browser UI tests
│   └── APIs/           # API tests
├── config.py           # Shared configuration and test data
├── utils.py            # Helper functions (API setup/teardown, email generation)
├── conftest.py         # Fixtures: browser, context, tracing, ad-blocking
└── pytest.ini          # pytest configuration and markers
```

---

## Test Suites

### UI Tests (`tests/UItests/`)
Browser tests using the Page Object Model:
- User registration and login
- Logout
- Incorrect login error handling
- Signup with existing email
- Product search
- Product details
- Add to cart / add multiple products to cart
- Contact Us form submission

### API Tests (`tests/APIs/`)
API tests using Playwright's built-in HTTP client:
- Products list
- Brands list
- Search product
- Verify login (valid, invalid, missing params)
- Create, update, delete user account
- Get user details by email

---

## Key Features

- **Page Object Model** — selectors and actions encapsulated in page classes
- **Auth state caching** — login session reused across tests for performance
- **API-driven setup/teardown** — users created and deleted via API, not UI
- **Tracing** — Playwright traces saved per test for debugging
- **Screenshots on failure** — automatically captured and added to HTML report
- **Ad blocking** — test-specific ad domains blocked to reduce noise
- **pytest markers** — run UI or API tests selectively with `-m ui` or `-m api`
- **Docker support** — run tests in a container for consistent environments

---

## Setup

**Prerequisites:** Python 3.9+

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

---

## Running Tests

```bash
# All tests
python3 -m pytest

# UI tests only
python3 -m pytest -m ui

# API tests only
python3 -m pytest -m api

# Specific file
python3 -m pytest tests/UItests/test_RegisterUser.py

# Headless mode
python3 -m pytest --headless=true

# With slow motion (useful for debugging)
python3 -m pytest --playwright-slowmo=500

# Generate HTML report
python3 -m pytest --html=report.html
```

---

## Running with Docker

```bash
docker-compose up
```

---

## Debugging

Playwright traces are saved to `traces/` after each test run:

```bash
playwright show-trace traces/<trace-file>.zip
```

---

## Configuration

Environment variables can override defaults:

| Variable | Default |
|----------|---------|
| `BASE_URL` | `https://automationexercise.com/` |
| `LOGIN_EMAIL` | `playwright@automationexercise.com` |
| `LOGIN_PASSWORD` | `Password123!` |
