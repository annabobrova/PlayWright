from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def verify_all_products_page(self) -> None:
        """Verify that the All Products page heading is visible."""
        expect(self.page.get_by_role("heading", name="All Products")).to_be_visible()

    def verify_products_list_visible(self) -> None:
        """Verify that the products grid container is visible on the page."""
        expect(self.page.locator(".features_items")).to_be_visible()

    def get_first_product_name_and_price(self) -> tuple[str, str]:
        """Return the name and price of the first product card as a (name, price) tuple."""
        first_card = self.page.locator(".features_items .product-image-wrapper").first
        name = first_card.locator(".productinfo p").inner_text().strip()
        price = first_card.locator(".productinfo h2").inner_text().strip()
        return name, price

    def open_first_product(self) -> None:
        """Click the View Product link for the first product in the list."""
        self.page.get_by_role("link", name="View Product").first.click()

    def verify_product_details_visible(self, expected_name: str, expected_price: str) -> None:
        """Verify the product detail page shows the correct name, price and required fields."""
        product_info = self.page.locator(".product-information")
        expect(product_info.get_by_role("heading", name=expected_name)).to_be_visible()
        expect(product_info).to_contain_text("Category:")
        expect(product_info).to_contain_text("Availability:")
        expect(product_info).to_contain_text("Condition:")
        expect(product_info).to_contain_text("Brand:")
        expect(product_info).to_contain_text(expected_price)

    def search_for_product(self, query: str) -> None:
        """Type a search query into the search box and submit it."""
        self.page.get_by_placeholder("Search Product").fill(query)
        self.page.locator("button#submit_search").click()

    def verify_searched_products_visible(self) -> None:
        """Verify the Searched Products heading and results grid are visible."""
        expect(self.page.get_by_role("heading", name="Searched Products")).to_be_visible(timeout=15000)
        expect(self.page.locator(".features_items")).to_be_visible()

    def verify_search_results_contain_name(self, expected_name: str) -> None:
        """Verify every product in the search results contains the expected name."""
        product_names = self.page.locator(".features_items .productinfo p")
        expect(product_names.first).to_be_visible()
        for name in product_names.all_inner_texts():
            assert expected_name.lower() in name.lower(), f"Unexpected product name: {name}"

    def add_to_cart(self) -> None:
        """Click the Add to cart button on the product detail page."""
        self.page.get_by_role("button", name="Add to cart").click()

    def get_product_name_by_index(self, index: int) -> str:
        """Return the name of the product card at the given zero-based index."""
        card = self.page.locator(".features_items .product-image-wrapper").nth(index)
        return card.locator(".productinfo p").inner_text().strip()

    def hover_and_add_to_cart(self, index: int) -> None:
        """Hover over the product card at the given index and click Add to Cart."""
        card = self.page.locator(".features_items .product-image-wrapper").nth(index)
        card.scroll_into_view_if_needed()
        card.hover()
        card.locator(".product-overlay a.add-to-cart").click()

    def verify_products_list_contains(self, expected_name: str, expected_price: str) -> None:
        """Verify the products grid contains a product with the given name and price."""
        products_block = self.page.locator(".features_items")
        expect(products_block).to_be_visible()
        expect(products_block).to_contain_text(expected_name)
        expect(products_block).to_contain_text(expected_price)
