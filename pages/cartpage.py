from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def verify_add_to_cart_modal(self) -> None:
        expect(self.page.get_by_text("Added!")).to_be_visible()

    def view_cart_from_modal(self) -> None:
        self.page.get_by_role("link", name="View Cart").click()

    def continue_shopping(self) -> None:
        self.page.get_by_role("button", name="Continue Shopping").click()

    def verify_product_in_cart(self, product_name: str) -> None:
        expect(self.page.locator(".cart_description").filter(has_text=product_name)).to_be_visible()
