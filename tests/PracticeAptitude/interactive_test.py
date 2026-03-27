"""
Interactive numerical test runner.
Pauses at each question, prints it to terminal, waits for your answer.

Usage: python3 tests/PracticeAptitude/interactive_test.py
"""
from playwright.sync_api import sync_playwright

AUTH_FILE = "tests/PracticeAptitude/auth.json"
BASE_URL = "https://www.practiceaptitudetests.com"


def get_question(page):
    """Extract question text from the page."""
    selectors = [
        ".question-text",
        ".question",
        "[class*='question']",
        "h2",
        "h3",
    ]
    for selector in selectors:
        el = page.locator(selector).first
        if el.count() > 0:
            text = el.inner_text().strip()
            if text:
                return text
    return page.locator("body").inner_text()[:1000]


def get_options(page):
    """Extract answer options from the page."""
    options = []

    # Try radio button labels
    radios = page.locator("input[type='radio']").all()
    for i, radio in enumerate(radios):
        label = page.locator(f"label[for='{radio.get_attribute('id')}']")
        if label.count() > 0:
            options.append((i + 1, label.inner_text().strip()))
        else:
            options.append((i + 1, radio.get_attribute("value") or f"Option {i + 1}"))

    return options


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()

    # Navigate to numerical tests page
    page.goto(f"{BASE_URL}/numerical-reasoning-tests/")
    page.wait_for_load_state("networkidle")

    print("\nBrowser is open on the numerical tests page.")
    print("1. Click the test you want in the browser")
    print("2. Click through any intro/instructions screens until you see the FIRST QUESTION")
    print("3. Then press Enter here to start answering...")
    input()

    page.wait_for_load_state("networkidle")

    question_num = 1
    while True:
        page.wait_for_load_state("networkidle")

        # Check if test is complete
        if any(word in page.url for word in ["result", "complete", "finish", "score"]):
            print("\n✓ Test complete! Check the browser for your results.")
            break

        # Extract and print question
        question_text = get_question(page)
        options = get_options(page)

        print(f"\n{'='*60}")
        print(f"Question {question_num}:")
        print(f"{question_text}")
        print()
        if options:
            for num, text in options:
                print(f"  {num}. {text}")
        else:
            print("(Could not extract options — check the browser window)")

        print()

        if not options:
            answer = input("Type your answer or press Enter to skip: ").strip()
        else:
            answer = input(f"Enter answer number (1-{len(options)}): ").strip()

        if answer.isdigit():
            idx = int(answer) - 1
            radios = page.locator("input[type='radio']").all()
            if 0 <= idx < len(radios):
                radios[idx].click()

        # Click Next or Finish
        for btn_name in ["Next", "Finish", "Submit", "Continue"]:
            btn = page.get_by_role("button", name=btn_name)
            if btn.count() > 0:
                btn.first.click()
                break

        question_num += 1

    input("\nPress Enter to close the browser...")
    browser.close()
