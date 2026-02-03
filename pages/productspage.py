from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def verify_all_products_page(self) -> None:
        expect(self.page.get_by_role("heading", name="All Products")).to_be_visible()

    def verify_products_list_visible(self) -> None:
        expect(self.page.locator(".features_items")).to_be_visible()

    def get_first_product_name_and_price(self) -> tuple[str, str]:
        first_card = self.page.locator(".features_items .product-image-wrapper").first
        name = first_card.locator(".productinfo p").inner_text().strip()
        price = first_card.locator(".productinfo h2").inner_text().strip()
        return name, price

    def open_first_product(self) -> None:
        self.page.get_by_role("link", name="View Product").first.click()

    def verify_product_details_visible(self, expected_name: str, expected_price: str) -> None:
        product_info = self.page.locator(".product-information")
        expect(product_info.get_by_role("heading", name=expected_name)).to_be_visible()
        expect(product_info).to_contain_text("Category:")
        expect(product_info).to_contain_text("Availability:")
        expect(product_info).to_contain_text("Condition:")
        expect(product_info).to_contain_text("Brand:")
        expect(product_info).to_contain_text(expected_price)
