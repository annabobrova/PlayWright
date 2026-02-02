from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.signuppage import SignupPage
from utils import generate_random_email, create_user_via_api, delete_user_via_api
from config import BASE_URL, TEST_PASSWORD, TEST_NAME_SIGNUP

def test_user_login(page: Page) -> None:
    home_page = HomePage(page)
    
    # 1. Setup: Create a new user via API
    api_request_context = page.request
    test_email = generate_random_email()
    
    print(f"Setup: Creating user {test_email} via API...")
    create_response = create_user_via_api(api_request_context, test_email)
    assert create_response.get("responseCode") == 201, f"API setup failed: {create_response}"
    
    # Initialize page object with the new credentials
    login_page = SignupPage(page, email=test_email)

    try:
        # 2. Navigate to home page
        page.goto(BASE_URL)
        expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

        # 3. Click on 'Signup / Login' button
        home_page.goto_signup_login()
        expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()

        # 4. Login with correct email and password
        print(f"Action: Logging in with {test_email}...")
        login_page.login_to_your_account()

        # 5. Verify that 'Logged in as username' is visible
        expect(page.locator("#header")).to_contain_text(f"Logged in as {TEST_NAME_SIGNUP}")
        print("Verification: Successfully logged in.")

    finally:
        # 6. Teardown: Delete the account via API (faster and more reliable than UI)
        print(f"Teardown: Deleting user {test_email} via API...")
        delete_json = delete_user_via_api(api_request_context, test_email)
        
        # Verify deletion was successful (optional but good practice)
        if delete_json.get("responseCode") == 200:
            print("Teardown: Account deleted successfully.")
        else:
            print(f"Teardown: Failed to delete account. Response: {delete_json}")
