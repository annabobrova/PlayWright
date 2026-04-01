from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def verify_add_to_cart_modal(self) -> None:
        """Verify the 'Added!' confirmation modal is visible after adding to cart."""
        expect(self.page.get_by_text("Added!")).to_be_visible()

    def view_cart_from_modal(self) -> None:
        """Click View Cart in the confirmation modal to navigate to the cart page."""
        self.page.get_by_role("link", name="View Cart").click()

    def continue_shopping(self) -> None:
        """Click Continue Shopping in the confirmation modal to dismiss it."""
        self.page.get_by_role("button", name="Continue Shopping").click()

    def verify_product_in_cart(self, product_name: str) -> None:
        """Verify that a product with the given name is present in the cart."""
        expect(self.page.locator(".cart_description").filter(has_text=product_name)).to_be_visible()
