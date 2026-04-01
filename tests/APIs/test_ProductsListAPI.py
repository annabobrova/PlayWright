import pytest
from playwright.sync_api import Page
from config import BASE_URL


@pytest.mark.api
def test_products_list_api_post_not_supported(page: Page) -> None:
    """API 2: Verify that POST to /api/productsList returns 405 - method not supported."""
    response = page.request.post(f"{BASE_URL}/api/productsList")

    body = response.json()
    assert body.get("responseCode") == 405, f"Expected 405, got: {body}"
    assert body.get("message") == "This request method is not supported.", f"Unexpected message: {body}"


@pytest.mark.api
def test_products_list_api_returns_products(page: Page) -> None:
    """API 1: Verify that GET /api/productsList returns 200 with a non-empty list of products containing id, name, price, brand and category."""
    response = page.request.get(f"{BASE_URL}/api/productsList")

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected responseCode 200, got: {body}"

    products = body.get("products")
    assert isinstance(products, list), f"Expected products to be a list, got: {type(products)}"
    assert len(products) > 0, "Expected at least one product in the list"

    first = products[0]
    assert "id" in first, f"Product missing 'id' field: {first}"
    assert "name" in first, f"Product missing 'name' field: {first}"
    assert "price" in first, f"Product missing 'price' field: {first}"
    assert "brand" in first, f"Product missing 'brand' field: {first}"
    assert "category" in first, f"Product missing 'category' field: {first}"
