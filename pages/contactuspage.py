from playwright.sync_api import Page


class ContactUsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def fill_contact_form(self, name: str, email: str, subject: str, message: str) -> None:
        self.page.locator("input[data-qa='name']").fill(name)
        self.page.locator("input[data-qa='email']").fill(email)
        self.page.locator("input[data-qa='subject']").fill(subject)
        self.page.locator("textarea[data-qa='message']").fill(message)

    def upload_file(self, file_path: str) -> None:
        file_input = self.page.locator("input[name='upload_file']")
        file_input.wait_for(state="visible")
        file_input.set_input_files(file_path)

    def submit_form_accept_dialog(self) -> None:
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.wait_for(state="visible")
        submit_button.scroll_into_view_if_needed()
        # Register handler before click so it fires immediately when dialog appears
        self.page.once("dialog", lambda dialog: dialog.accept())
        submit_button.click()

    def click_home(self) -> None:
        self.page.locator("a.btn.btn-success").click()
