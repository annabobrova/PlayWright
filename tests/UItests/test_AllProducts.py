from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.productspage import ProductsPage
from config import BASE_URL


def test_all_products_and_product_detail(page: Page) -> None:
    """
    Test navigation to All Products, open first product, verify detail fields,
    and confirm the product name and price match the list view.
    """
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # 1. Navigate to home page
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()

    # 2. Click on 'Products' button
    home_page.goto_products()

    # 3. Verify user is navigated to ALL PRODUCTS page successfully
    products_page.verify_all_products_page()

    # 4. The products list is visible
    products_page.verify_products_list_visible()

    # 5. Capture first product name and price, then open product
    first_name, first_price = products_page.get_first_product_name_and_price()
    products_page.open_first_product()

    # 6. User is landed to product detail page and details are visible
    products_page.verify_product_details_visible(first_name, first_price)
    print(f"Verification: Product details with name '{first_name}' and price '{first_price}' were displayed.")
