from playwright.sync_api import Page
from pages.homepage import HomePage
from pages.productspage import ProductsPage
from pages.cartpage import CartPage
from config import BASE_URL


def test_add_multiple_products_to_cart(logged_in_page: Page) -> None:
    """
    Verify that three products from different parts of the listing page
    can be added to cart using the hover overlay, with scrolling between them.
    """
    home_page = HomePage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)

    # Navigate to products page
    logged_in_page.goto(BASE_URL)
    home_page.goto_products()
    products_page.verify_all_products_page()

    # Capture names of 3 products spread across the page
    product_indices = [0, 5, 10]
    product_names = [products_page.get_product_name_by_index(i) for i in product_indices]

    # Add first product (top of page)
    products_page.hover_and_add_to_cart(product_indices[0])
    cart_page.verify_add_to_cart_modal()
    cart_page.continue_shopping()

    # Add second product (mid page — scrolls automatically)
    products_page.hover_and_add_to_cart(product_indices[1])
    cart_page.verify_add_to_cart_modal()
    cart_page.continue_shopping()

    # Add third product (further down — scrolls automatically)
    products_page.hover_and_add_to_cart(product_indices[2])
    cart_page.verify_add_to_cart_modal()
    cart_page.view_cart_from_modal()

    # Verify all 3 products are in the cart
    for name in product_names:
        cart_page.verify_product_in_cart(name)
