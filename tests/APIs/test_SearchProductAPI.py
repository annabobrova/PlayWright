import json
import os
import pytest
from playwright.sync_api import Page
from config import BASE_URL


def _load_search_data() -> list[str]:
    data_file = os.path.join(os.path.dirname(__file__), "test_data", "search_products.json")
    with open(data_file) as f:
        return [item["search_term"] for item in json.load(f)]


@pytest.mark.api
@pytest.mark.parametrize("search_term", _load_search_data())
def test_search_product(page: Page, search_term: str) -> None:
    """Verify that POST /api/searchProduct returns 200 with results for each search term."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct", form={"search_product": search_term})

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected responseCode 200, got: {body}"

    products = body.get("products")
    assert isinstance(products, list), f"Expected products to be a list, got: {type(products)}"
    assert len(products) > 0, f"Expected at least one product for search term '{search_term}'"


@pytest.mark.api
def test_search_product_missing_param(page: Page) -> None:
    """Verify that POST /api/searchProduct without the search_product param returns 400 - bad request."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct")

    body = response.json()
    assert body.get("responseCode") == 400, f"Expected 400, got: {body}"
    assert body.get("message") == "Bad request, search_product parameter is missing in POST request.", f"Unexpected message: {body}"
