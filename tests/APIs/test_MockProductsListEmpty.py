import json
from playwright.sync_api import Page
from config import BASE_URL


def test_mock_products_list_api_empty(page: Page) -> None:
    """
    Mock the products list API with an empty list and verify the response.
    """
    mocked_products = {
        "responseCode": 200,
        "products": []
    }

    def handle_products_list(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_products)
        )

    page.route("**/api/productsList", handle_products_list)

    # Trigger the mocked API via request context and verify response
    response = page.request.get(f"{BASE_URL}api/productsList")
    mocked_response = response.json()

    assert response.status == 200
    assert mocked_response.get("responseCode") == 200
    assert mocked_response.get("products") == []
