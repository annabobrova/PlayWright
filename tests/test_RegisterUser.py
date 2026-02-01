import re
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.signuppage import SignupPage
from utils import generate_random_email
from config import (
    BASE_URL, TEST_FIRST_NAME
)

# Create a single randomly generated email to be used for the test run
GENERATED_TEST_EMAIL = generate_random_email()

"""
Test user registration flow on AutomationExercise website.
This test uses a unique email for each run to ensure independence.
"""
def test_example(page: Page) -> None:
    home_page = HomePage(page)
    # Pass the unique email to the page object
    signup_page = SignupPage(page, email=GENERATED_TEST_EMAIL)

    try:
        # === Main Test Logic ===
        page.goto(BASE_URL)
        expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()
        
        home_page.goto_signup_login()
        expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()

        # Fill in the signup form with the unique email
        signup_page.signup_new_user()
        
        # The "Email Address already exist!" message should not appear with unique emails.
        expect(page.get_by_text("Email Address already exist!")).not_to_be_visible()

        # Verify account information form is displayed
        expect(page.get_by_text("Enter Account Information")).to_be_visible()

        # Fill in account information and create account
        signup_page.fill_account_information_and_create()
        
        # Verify account was created
        expect(page.get_by_text("Account Created!")).to_be_visible()
        signup_page.continue_after_registration()

        # Verify user is logged in with correct name
        expect(page.locator("#header")).to_contain_text(f"Logged in as {TEST_FIRST_NAME}")

    finally:
        # === Teardown: Post-test cleanup ===
        print(f"Teardown: Attempting to delete user '{GENERATED_TEST_EMAIL}'.")
        page.goto(BASE_URL)
        
        home_page.delete_account()
        expect(page.get_by_text("Account Deleted!")).to_be_visible()
        print(f"Teardown: User '{GENERATED_TEST_EMAIL}' successfully deleted.")