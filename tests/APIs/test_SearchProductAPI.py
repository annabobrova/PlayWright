import pytest
from playwright.sync_api import Page
from config import BASE_URL


@pytest.mark.api
def test_search_product(page: Page) -> None:
    """Verify that POST /api/searchProduct with a valid search_product param returns 200 with a matching products list."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct", form={"search_product": "top"})

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected responseCode 200, got: {body}"

    products = body.get("products")
    assert isinstance(products, list), f"Expected products to be a list, got: {type(products)}"
    assert len(products) > 0, "Expected at least one matching product"


@pytest.mark.api
def test_search_product_missing_param(page: Page) -> None:
    """Verify that POST /api/searchProduct without the search_product param returns 400 - bad request."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct")

    body = response.json()
    assert body.get("responseCode") == 400, f"Expected 400, got: {body}"
    assert body.get("message") == "Bad request, search_product parameter is missing in POST request.", f"Unexpected message: {body}"
