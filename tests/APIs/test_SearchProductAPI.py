import json
import jsonschema
import os
import pytest
from playwright.sync_api import Page
from config import BASE_URL
from schemas import PRODUCTS_RESPONSE_SCHEMA


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

    jsonschema.validate(body, PRODUCTS_RESPONSE_SCHEMA)

    assert len(body["products"]) > 0, f"Expected at least one product for search term '{search_term}'"


@pytest.mark.api
def test_search_product_missing_param(page: Page) -> None:
    """Verify that POST /api/searchProduct without the search_product param returns 400 - bad request."""
    response = page.request.post(f"{BASE_URL}/api/searchProduct")

    body = response.json()
    assert body.get("responseCode") == 400, f"Expected 400, got: {body}"
    assert body.get("message") == "Bad request, search_product parameter is missing in POST request.", f"Unexpected message: {body}"


@pytest.mark.api
def test_search_product_mocked_response(page: Page) -> None:
    """
    Verify that page.route() intercepts a browser-initiated fetch and returns fake data.

    page.route() only works for requests made by the browser itself — not for
    page.request (the APIRequestContext), which bypasses Playwright routing.
    We use page.evaluate() to trigger a fetch() from within the browser so the
    route handler can intercept it.
    """
    fake_body = json.dumps({
        "responseCode": 200,
        "products": [
            {"id": 1, "name": "Fake Top", "price": "Rs. 500"},
            {"id": 2, "name": "Fake Dress", "price": "Rs. 1000"}
        ]
    })

    page.route("**/api/searchProduct", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=fake_body
    ))

    page.goto(BASE_URL)

    result = page.evaluate("""async () => {
        const form = new FormData();
        form.append('search_product', 'top');
        const res = await fetch('/api/searchProduct', { method: 'POST', body: form });
        return { status: res.status, body: await res.json() };
    }""")

    assert result["status"] == 200
    body = result["body"]
    assert body.get("responseCode") == 200
    products = body.get("products")
    assert len(products) == 2
    assert products[0]["name"] == "Fake Top"


@pytest.mark.api
def test_search_product_mocked_server_error(page: Page) -> None:
    """
    Verify that page.route() can simulate a 500 error — a scenario impossible to trigger on the real site.

    Same pattern as test_search_product_mocked_response: the fetch is triggered
    from within the browser via page.evaluate() so page.route() can intercept it.
    """
    page.route("**/api/searchProduct", lambda route: route.fulfill(
        status=500,
        content_type="application/json",
        body=json.dumps({"responseCode": 500, "message": "Internal Server Error"})
    ))

    page.goto(BASE_URL)

    result = page.evaluate("""async () => {
        const form = new FormData();
        form.append('search_product', 'top');
        const res = await fetch('/api/searchProduct', { method: 'POST', body: form });
        return { status: res.status, body: await res.json() };
    }""")

    assert result["status"] == 500
    body = result["body"]
    assert body.get("responseCode") == 500
    assert body.get("message") == "Internal Server Error"
