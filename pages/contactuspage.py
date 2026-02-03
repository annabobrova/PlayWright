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
        self.page.locator("input[name='upload_file']").set_input_files(file_path)

    def submit_form_accept_dialog(self) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name="Submit").click()

    def click_home(self) -> None:
        self.page.locator("a.btn.btn-success").click()
