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

    def search_for_product(self, query: str) -> None:
        self.page.get_by_placeholder("Search Product").fill(query)
        self.page.locator("button#submit_search").click()

    def verify_searched_products_visible(self) -> None:
        expect(self.page.get_by_role("heading", name="Searched Products")).to_be_visible()
        expect(self.page.locator(".features_items")).to_be_visible()

    def verify_search_results_contain_name(self, expected_name: str) -> None:
        product_names = self.page.locator(".features_items .productinfo p")
        expect(product_names.first).to_be_visible()
        for name in product_names.all_inner_texts():
            assert expected_name.lower() in name.lower(), f"Unexpected product name: {name}"

    def verify_products_list_contains(self, expected_name: str, expected_price: str) -> None:
        products_block = self.page.locator(".features_items")
        expect(products_block).to_be_visible()
        expect(products_block).to_contain_text(expected_name)
        expect(products_block).to_contain_text(expected_price)
