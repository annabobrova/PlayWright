from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from config import BASE_URL


def test_products_list_empty_ui(page: Page) -> None:
    """
    Mock the Products page HTML to show no products and verify the UI is empty.
    """
    home_page = HomePage(page)

    empty_products_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>All Products</title>
      </head>
      <body>
        <section>
          <h2 class="title text-center">All Products</h2>
          <div class="features_items">
            <!-- No product cards -->
          </div>
        </section>
      </body>
    </html>
    """

    def handle_products_page(route):
        route.fulfill(
            status=200,
            content_type="text/html",
            body=empty_products_html
        )

    page.route("**/products", handle_products_page)

    # 1. Navigate to home page
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

    # 2. Click on 'Products' button
    home_page.goto_products()

    # 3. Verify All Products page is visible and no products are shown
    expect(page.get_by_role("heading", name="All Products")).to_be_visible()
    product_cards = page.locator(".product-image-wrapper")
    expect(product_cards).to_have_count(0)
