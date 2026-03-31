from pathlib import Path
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.contactuspage import ContactUsPage
from utils import generate_random_email
from config import BASE_URL, TEST_NAME_SIGNUP


def test_contact_us_form_submission(page: Page) -> None:
    """
    Test the Contact Us form by submitting details, uploading a file,
    confirming the success message, and returning to the home page.
    """
    home_page = HomePage(page)
    contact_us_page = ContactUsPage(page)

    test_email = generate_random_email()
    # requirements.txt is used as the upload file because it is always present in the project root,
    # both locally and inside the Docker container, making the test environment-agnostic.
    file_to_upload = Path(__file__).resolve().parents[2] / "requirements.txt"

    # 1. Navigate to home page
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

    # 2. Click on 'Contact Us' button
    home_page.goto_contact_us()
    expect(page.get_by_role("heading", name="GET IN TOUCH")).to_be_visible()

    # 3. Enter name, email, subject and message
    contact_us_page.fill_contact_form(
        name=TEST_NAME_SIGNUP,
        email=test_email,
        subject="Test Subject",
        message="Test message from Playwright UI test."
    )

    # 4. Upload file
    contact_us_page.upload_file(str(file_to_upload))

    # 5. Click 'Submit' button and accept dialog
    contact_us_page.submit_form_accept_dialog()

    # 6. Verify success message
    page.wait_for_load_state("networkidle")
    success_alert = page.locator(
        ".status.alert-success",
        has_text="Success! Your details have been submitted successfully."
    )
    expect(success_alert).to_be_visible(timeout=15000)

    # 7. Click 'Home' button and verify landing page
    contact_us_page.click_home()
    expect(page.get_by_role("heading", name="AutomationExercise").first).to_be_visible()
