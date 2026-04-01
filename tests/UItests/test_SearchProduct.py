import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.productspage import ProductsPage
from config import BASE_URL


@pytest.mark.ui
@pytest.mark.parametrize("query", ["top", "dress", "jeans"])
def test_search_product(page: Page, query: str) -> None:
    """
    Verify that searching for a product term returns relevant results.
    Runs for each query: top, dress, jeans.
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

    # 4. Enter product name in search input and click search button
    products_page.search_for_product(query)

    # 5. Verify 'SEARCHED PRODUCTS' is visible and results are shown
    products_page.verify_searched_products_visible()

    # 6. Verify all the products related to search are visible
    products_page.verify_search_results_contain_name(query)
