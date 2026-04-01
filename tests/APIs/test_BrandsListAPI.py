import pytest
from playwright.sync_api import Page
from config import BASE_URL


@pytest.mark.api
def test_api_3_get_brands_list(page: Page) -> None:
    """API 3: Verify that GET /api/brandsList returns 200 with a non-empty list of brands containing id and brand name."""
    response = page.request.get(f"{BASE_URL}/api/brandsList")

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected responseCode 200, got: {body}"

    brands = body.get("brands")
    assert isinstance(brands, list), f"Expected brands to be a list, got: {type(brands)}"
    assert len(brands) > 0, "Expected at least one brand in the list"

    first = brands[0]
    assert "id" in first, f"Brand missing 'id' field: {first}"
    assert "brand" in first, f"Brand missing 'brand' field: {first}"


@pytest.mark.api
def test_api_4_put_brands_not_supported(page: Page) -> None:
    """API 4: Verify that PUT to /api/brandsList returns 405 - method not supported."""
    response = page.request.put(f"{BASE_URL}/api/brandsList")

    body = response.json()
    assert body.get("responseCode") == 405, f"Expected 405, got: {body}"
    assert body.get("message") == "This request method is not supported.", f"Unexpected message: {body}"
