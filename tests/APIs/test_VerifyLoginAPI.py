import pytest
from playwright.sync_api import Page
from config import BASE_URL, TEST_PASSWORD


@pytest.mark.api
def test_verify_login_valid(page: Page, registered_user: str) -> None:
    """Verify that POST /api/verifyLogin with valid credentials returns 200 - User exists!"""
    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"email": registered_user, "password": TEST_PASSWORD}
    )

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected 200, got: {body}"
    assert body.get("message") == "User exists!", f"Unexpected message: {body}"


@pytest.mark.api
def test_verify_login_missing_email(page: Page) -> None:
    """Verify that POST /api/verifyLogin without the email param returns 400 - bad request."""
    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"password": TEST_PASSWORD}
    )

    body = response.json()
    assert body.get("responseCode") == 400, f"Expected 400, got: {body}"
    assert body.get("message") == "Bad request, email or password parameter is missing in POST request.", f"Unexpected message: {body}"


@pytest.mark.api
def test_delete_verify_login_not_supported(page: Page) -> None:
    """Verify that DELETE to /api/verifyLogin returns 405 - method not supported."""
    response = page.request.delete(f"{BASE_URL}/api/verifyLogin")

    body = response.json()
    assert body.get("responseCode") == 405, f"Expected 405, got: {body}"
    assert body.get("message") == "This request method is not supported.", f"Unexpected message: {body}"


@pytest.mark.api
def test_verify_login_invalid_credentials(page: Page) -> None:
    """Verify that POST /api/verifyLogin with invalid credentials returns 404 - User not found!"""
    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"email": "nonexistent@example.com", "password": "wrongpassword"}
    )

    body = response.json()
    assert body.get("responseCode") == 404, f"Expected 404, got: {body}"
    assert body.get("message") == "User not found!", f"Unexpected message: {body}"
