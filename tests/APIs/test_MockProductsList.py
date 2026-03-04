import json
from playwright.sync_api import Page
from pages.homepage import HomePage
from config import BASE_URL
from tests.conftest import page


def test_mock_products_list_api(page: Page) -> None:
    """
    Mock the products list API and verify the mocked response data is returned.
    """
    
    mocked_products = {
        "responseCode": 200,
        "products": [
            {
                "id": 9991,
                "name": "Winter Top",
                "price": "Rs. 999",
                "brand": "MockBrand",
                "category": {
                    "usertype": {"usertype": "Women"},
                    "category": "Tops"
                }
            },
            {
                "id": 9992,
                "name": "Summer Top",
                "price": "Rs. 888",
                "brand": "MockBrand",
                "category": {
                    "usertype": {"usertype": "Women"},
                    "category": "Tops"
                }
            }
        ]
    }

    def handle_products_list(route):
        print(f"✅ SUCCESSFULLY MOCKED: {route.request.url}")
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_products)
        )

    page.route("**/api/productsList*", handle_products_list)
    
    # Trigger the mocked API via request context and verify response
    response = page.request.get(f"{BASE_URL}api/productsList")

    mocked_response = response.json()
    home_page = HomePage(page)
   
    # 1. Navigate to home page
    page.goto(BASE_URL, wait_until="networkidle")

    # 2. Click on 'Products' button
    home_page.goto_products()

    assert response.status == 200
    assert mocked_response.get("responseCode") == 200
    assert mocked_response.get("products")[0]["name"] == "Winter Top"
    assert mocked_response.get("products")[0]["price"] == "Rs. 999"
