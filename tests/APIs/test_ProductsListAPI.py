from playwright.sync_api import Page
from config import BASE_URL


def test_products_list_api_post_not_supported(page: Page) -> None:
    response = page.request.post(f"{BASE_URL}/api/productsList")

    body = response.json()
    assert body.get("responseCode") == 405
    assert body.get("message") == "This request method is not supported."


def test_products_list_api_returns_products(page: Page) -> None:
    response = page.request.get(f"{BASE_URL}/api/productsList")

    assert response.status == 200

    body = response.json()
    assert body.get("responseCode") == 200

    products = body.get("products")
    assert isinstance(products, list)
    assert len(products) > 0

    first = products[0]
    assert "id" in first
    assert "name" in first
    assert "price" in first
    assert "brand" in first
    assert "category" in first
