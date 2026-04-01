from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto_signup_login(self) -> None:
        """Click on Signup/Login link to navigate to the signup/login page."""
        self.page.get_by_role("link", name=" Signup / Login").click()

    def goto_contact_us(self) -> None:
        """Click on Contact Us link to navigate to the contact page."""
        self.page.get_by_role("link", name=" Contact us").click()

    def goto_products(self) -> None:
        """Click on Products link to navigate to the products page."""
        self.page.get_by_role("link", name=" Products").click()

    def delete_account(self) -> None:
        """Click on Delete Account link to delete the current user's account."""
        self.page.get_by_role("link", name=" Delete Account").click()

    def logout(self) -> None:
        """Click on Logout link to end the current session."""
        self.page.get_by_role("link", name=" Logout").click()
