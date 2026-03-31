from playwright.sync_api import Page
from pages.homepage import HomePage
from pages.productspage import ProductsPage
from pages.cartpage import CartPage
from config import BASE_URL


def test_add_product_to_cart(logged_in_page: Page) -> None:
    """
    Verify that a product can be added to cart from the product detail page,
    the confirmation modal appears, and the product shows in the cart.
    """
    home_page = HomePage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)

    # Navigate to products
    logged_in_page.goto(BASE_URL)
    home_page.goto_products()
    products_page.verify_all_products_page()

    # Get first product name, then open it
    first_name, _ = products_page.get_first_product_name_and_price()
    products_page.open_first_product()

    # Add to cart
    products_page.add_to_cart()

    # Verify modal and go to cart
    cart_page.verify_add_to_cart_modal()
    cart_page.view_cart_from_modal()

    # Verify product is in cart
    cart_page.verify_product_in_cart(first_name)
