from playwright.sync_api import Page, expect
from utils import generate_random_email
from config import (
    TEST_PASSWORD, TEST_NAME_SIGNUP,
    TEST_FIRST_NAME, TEST_LAST_NAME, TEST_COMPANY, TEST_ADDRESS,
    TEST_STATE, TEST_CITY, TEST_ZIPCODE, TEST_PHONE,
    TEST_COUNTRY, TEST_DAY, TEST_MONTH, TEST_YEAR
)


class SignupPage:
    def __init__(self, page: Page, email: str) -> None:
        self.page = page
        self.email = email

    def signup_new_user(self) -> None:
        """
        Fill in the signup form with test name and email.
        """
        self.page.get_by_role("textbox", name="Name").fill(TEST_NAME_SIGNUP)
        self.page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(self.email)
        self.page.get_by_role("button", name="Signup").click()
        print(f"SignupPage: Filled signup form with Name='{TEST_NAME_SIGNUP}' and Email='{self.email}'.")

    def verify_account_information_form(self) -> None:
        """
        Verify that the account information form is displayed after signup.
        """
        expect(self.page.get_by_text("Enter Account Information")).to_be_visible()

    def fill_account_information_and_create(self) -> None:
        """
        Fill in the account information form.
        """
        self.page.get_by_role("radio", name="Mrs.").check()
        self.page.get_by_role("textbox", name="Password *").click()
        self.page.get_by_role("textbox", name="Password *").fill(TEST_PASSWORD)
        self.page.locator("#days").select_option(TEST_DAY)
        self.page.locator("#months").select_option(TEST_MONTH)
        self.page.locator("#years").select_option(TEST_YEAR)
        self.page.get_by_role("checkbox", name="Sign up for our newsletter!").check()
        self.page.get_by_role("checkbox", name="Receive special offers from").check()
        self.page.get_by_role("textbox", name="First name *").click()
        self.page.get_by_role("textbox", name="First name *").fill(TEST_FIRST_NAME)
        self.page.get_by_role("textbox", name="First name *").press("Tab")
        self.page.get_by_role("textbox", name="Last name *").fill(TEST_LAST_NAME)
        self.page.get_by_role("textbox", name="Last name *").press("Tab")
        self.page.get_by_role("textbox", name="Company", exact=True).fill(TEST_COMPANY)
        self.page.get_by_role("textbox", name="Company", exact=True).press("Tab")
        self.page.get_by_role("textbox", name="Address * (Street address, P.").fill(TEST_ADDRESS)
        self.page.get_by_role("textbox", name="Address * (Street address, P.").press("Tab")
        self.page.get_by_role("textbox", name="Address 2").fill("address2")
        self.page.get_by_role("textbox", name="Address 2").press("Tab")
        self.page.get_by_label("Country *").select_option(TEST_COUNTRY)
        self.page.get_by_role("textbox", name="State *").click()
        self.page.get_by_role("textbox", name="State *").fill(TEST_STATE)
        self.page.get_by_role("textbox", name="City * Zipcode *").click()
        self.page.get_by_role("textbox", name="City * Zipcode *").fill(TEST_CITY)
        self.page.get_by_role("textbox", name="City * Zipcode *").press("Tab")
        self.page.locator("#zipcode").fill(TEST_ZIPCODE)
        self.page.locator("#zipcode").press("Tab")
        self.page.get_by_role("textbox", name="Mobile Number *").fill(TEST_PHONE)
        self.page.get_by_role("button", name="Create Account").click()

    def continue_after_registration(self) -> None:
        """
        Click the Continue button after successful account creation.
        """
        self.page.get_by_role("link", name="Continue").click()
        

    def login_to_your_account(self) -> None:
        """
        Login to existing account using credentials.
        """
        self.page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(self.email)
        self.page.get_by_role("textbox", name="Password").fill(TEST_PASSWORD)
        self.page.get_by_role("button", name="Login").click()
