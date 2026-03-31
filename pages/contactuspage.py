from playwright.sync_api import Page


class ContactUsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def fill_contact_form(self, name: str, email: str, subject: str, message: str) -> None:
        self.page.get_by_placeholder("Name").fill(name)
        self.page.get_by_role("textbox", name="Email", exact=True).fill(email)
        self.page.get_by_placeholder("Subject").fill(subject)
        self.page.get_by_placeholder("Your Message Here").fill(message)

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
