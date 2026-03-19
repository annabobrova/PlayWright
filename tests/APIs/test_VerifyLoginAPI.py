from playwright.sync_api import Page
from utils import generate_random_email, create_user_via_api, delete_user_via_api
from config import BASE_URL, TEST_PASSWORD


def test_api_7_verify_login_valid(page: Page) -> None:
    """API 7: Verify that POST /api/verifyLogin with valid credentials returns 200 - User exists!"""
    email = generate_random_email()
    create_user_via_api(page.request, email)

    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"email": email, "password": TEST_PASSWORD}
    )

    body = response.json()
    assert body.get("responseCode") == 200
    assert body.get("message") == "User exists!"

    delete_user_via_api(page.request, email)


def test_api_8_verify_login_missing_email(page: Page) -> None:
    """API 8: Verify that POST /api/verifyLogin without the email param returns 400 - bad request."""
    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"password": TEST_PASSWORD}
    )

    body = response.json()
    assert body.get("responseCode") == 400
    assert body.get("message") == "Bad request, email or password parameter is missing in POST request."


def test_api_9_delete_verify_login_not_supported(page: Page) -> None:
    """API 9: Verify that DELETE to /api/verifyLogin returns 405 - method not supported."""
    response = page.request.delete(f"{BASE_URL}/api/verifyLogin")

    body = response.json()
    assert body.get("responseCode") == 405
    assert body.get("message") == "This request method is not supported."


def test_api_10_verify_login_invalid_credentials(page: Page) -> None:
    """API 10: Verify that POST /api/verifyLogin with invalid credentials returns 404 - User not found!"""
    response = page.request.post(
        f"{BASE_URL}/api/verifyLogin",
        form={"email": "nonexistent@example.com", "password": "wrongpassword"}
    )

    body = response.json()
    assert body.get("responseCode") == 404
    assert body.get("message") == "User not found!"
