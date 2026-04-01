import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.signuppage import SignupPage
from utils import generate_random_email
from config import BASE_URL, TEST_PASSWORD

@pytest.mark.ui
def test_incorrect_login_with_unregistered_email(page: Page) -> None:
    """
    Test login with an unregistered email and verify the incorrect credentials error.
    """
    home_page = HomePage(page)
    # Generate a random email that definitely doesn't exist in the system
    random_email = generate_random_email()
    signup_page = SignupPage(page, email=random_email)

    # 1. Navigate to home page
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

    # 2. Click on 'Signup / Login' button
    home_page.goto_signup_login()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()

    # 3. Enter random email and password
    # The login_to_your_account method uses self.email (which is our random one)
    # and TEST_PASSWORD from config (which is what we want).
    signup_page.login_to_your_account()

    # 4. Verify error 'Your email or password is incorrect!' is visible
    # Note: The exact text on the site is "Your email or password is incorrect!"
    expect(page.get_by_text("Your email or password is incorrect!")).to_be_visible()
