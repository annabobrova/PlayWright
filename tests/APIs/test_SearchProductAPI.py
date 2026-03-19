from playwright.sync_api import Page
from config import BASE_URL


def test_api_5_search_product(page: Page) -> None:
    """API 5: Verify that POST /api/searchProduct with a valid search_product param returns 200 with a matching products list."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct", form={"search_product": "top"})

    assert response.status == 200

    body = response.json()
    assert body.get("responseCode") == 200

    products = body.get("products")
    assert isinstance(products, list)
    assert len(products) > 0


def test_api_6_search_product_missing_param(page: Page) -> None:
    """API 6: Verify that POST /api/searchProduct without the search_product param returns 400 - bad request."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct")

    body = response.json()
    assert body.get("responseCode") == 400
    assert body.get("message") == "Bad request, search_product parameter is missing in POST request."
