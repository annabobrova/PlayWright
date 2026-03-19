from playwright.sync_api import Page
from config import BASE_URL


def test_api_3_get_brands_list(page: Page) -> None:
    """API 3: Verify that GET /api/brandsList returns 200 with a non-empty list of brands containing id and brand name."""
    response = page.request.get(f"{BASE_URL}/api/brandsList")

    assert response.status == 200

    body = response.json()
    assert body.get("responseCode") == 200

    brands = body.get("brands")
    assert isinstance(brands, list)
    assert len(brands) > 0

    first = brands[0]
    assert "id" in first
    assert "brand" in first


def test_api_4_put_brands_not_supported(page: Page) -> None:
    """API 4: Verify that PUT to /api/brandsList returns 405 - method not supported."""
    response = page.request.put(f"{BASE_URL}/api/brandsList")

    body = response.json()
    assert body.get("responseCode") == 405
    assert body.get("message") == "This request method is not supported."
