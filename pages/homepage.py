from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto_signup_login(self) -> None:
        """Click on Signup/Login link to navigate to the signup/login page."""
        self.page.get_by_role("link", name=" Signup / Login").click()

    def delete_account(self) -> None:
        # Click on the Delete Account link
        self.page.get_by_role("link", name=" Delete Account").click()