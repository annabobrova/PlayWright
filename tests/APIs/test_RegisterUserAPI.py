import logging
import pytest
from playwright.sync_api import Page
from utils import generate_random_email, create_user_via_api, delete_user_via_api
from config import BASE_URL, TEST_PASSWORD

logger = logging.getLogger(__name__)

@pytest.mark.api
def test_create_register_user_account(page: Page) -> None:
    """Verify that POST /api/createAccount creates a new user and returns 201 - User created!"""
    # Get the API request context from the page (or use playwright.request)
    api_request_context = page.request
    
    # 1. Generate a unique email
    test_email = generate_random_email()
    
    # 2. Perform the POST request using the helper from utils
    response_json = create_user_via_api(api_request_context, test_email)
    
    # 3. Verify Response Code (Site returns 200 OK but body contains responseCode 201)
    # The requirement says Response Code: 201, but the API body field is what tracks this.
    assert response_json.get("responseCode") == 201, f"Expected 201, got: {response_json}"
    assert response_json.get("message") == "User created!", f"Unexpected message: {response_json}"

    logger.info("User created via API: %s", test_email)

    # Teardown: Delete the account using the delete API to keep the system clean
    delete_json = delete_user_via_api(api_request_context, test_email)
    assert delete_json.get("responseCode") == 200, f"Expected 200, got: {delete_json}"
    assert delete_json.get("message") == "Account deleted!", f"Unexpected message: {delete_json}"