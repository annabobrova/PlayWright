import logging
import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.signuppage import SignupPage
from utils import generate_random_email, create_user_via_api, delete_user_via_api
from config import BASE_URL

logger = logging.getLogger(__name__)


@pytest.mark.ui
def test_signup_with_existing_email_shows_error(page: Page) -> None:
    """
    Test signup with an existing email and verify the duplicate email error.
    """
    home_page = HomePage(page)

    # Setup: Create a user via API so the email is already registered
    api_request_context = page.request
    test_email = generate_random_email()
    logger.info("Setup: Creating user %s via API...", test_email)
    create_response = create_user_via_api(api_request_context, test_email)
    assert create_response.get("responseCode") == 201, f"API setup failed: {create_response}"

    signup_page = SignupPage(page, email=test_email)

    try:
        # 1. Navigate to home page
        page.goto(BASE_URL)
        expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

        # 2. Click on 'Signup / Login' button
        home_page.goto_signup_login()
        expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()

        # 3. Enter name and already registered email address
        # 4. Click 'Signup' button
        signup_page.signup_new_user()

        # 5. Verify error 'Email Address already exist!' is visible
        expect(page.get_by_text("Email Address already exist!")).to_be_visible()
        logger.info("Verification: Error message for existing email is visible.")
    finally:
        # Teardown: Delete the account via API
        logger.info("Teardown: Deleting user %s via API...", test_email)
        delete_json = delete_user_via_api(api_request_context, test_email)
        if delete_json.get("responseCode") == 200:
            logger.info("Teardown: Account deleted successfully.")
        else:
            logger.warning("Teardown: Failed to delete account. Response: %s", delete_json)
