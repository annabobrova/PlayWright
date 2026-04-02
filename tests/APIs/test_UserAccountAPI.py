import jsonschema
import pytest
from playwright.sync_api import Page
from utils import generate_random_email, create_user_via_api, delete_user_via_api
from schemas import USER_DETAIL_RESPONSE_SCHEMA
from config import (
    BASE_URL, TEST_PASSWORD, TEST_NAME_SIGNUP, TEST_FIRST_NAME, TEST_LAST_NAME,
    TEST_COMPANY, TEST_ADDRESS, TEST_COUNTRY, TEST_STATE, TEST_CITY,
    TEST_ZIPCODE, TEST_PHONE, TEST_DAY, TEST_MONTH, TEST_YEAR
)


@pytest.mark.api
def test_delete_user_account(page: Page) -> None:
    """Verify that DELETE /api/deleteAccount with valid credentials returns 200 - Account deleted!"""
    email = generate_random_email()
    create_user_via_api(page.request, email)

    delete_json = delete_user_via_api(page.request, email)
    assert delete_json.get("responseCode") == 200, f"Expected 200, got: {delete_json}"
    assert delete_json.get("message") == "Account deleted!", f"Unexpected message: {delete_json}"


@pytest.mark.api
def test_update_user_account(page: Page, registered_user: str) -> None:
    """Verify that PUT /api/updateAccount with full user details returns 200 - User updated!"""
    payload = {
        "name": TEST_NAME_SIGNUP,
        "email": registered_user,
        "password": TEST_PASSWORD,
        "title": "Mrs",
        "birth_date": TEST_DAY,
        "birth_month": TEST_MONTH,
        "birth_year": TEST_YEAR,
        "firstname": TEST_FIRST_NAME,
        "lastname": TEST_LAST_NAME,
        "company": TEST_COMPANY,
        "address1": TEST_ADDRESS,
        "address2": "Apt 202",
        "country": TEST_COUNTRY,
        "zipcode": TEST_ZIPCODE,
        "state": TEST_STATE,
        "city": TEST_CITY,
        "mobile_number": TEST_PHONE
    }
    response = page.request.put(f"{BASE_URL}/api/updateAccount", form=payload)

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected 200, got: {body}"
    assert body.get("message") == "User updated!", f"Unexpected message: {body}"


@pytest.mark.api
def test_get_user_detail_by_email(page: Page, registered_user: str) -> None:
    """Verify that GET /api/getUserDetailByEmail with a valid email returns 200 with user details including id, name and email."""
    response = page.request.get(f"{BASE_URL}/api/getUserDetailByEmail", params={"email": registered_user})

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    body = response.json()
    assert body.get("responseCode") == 200, f"Expected responseCode 200, got: {body}"

    jsonschema.validate(body, USER_DETAIL_RESPONSE_SCHEMA)

    assert body["user"]["email"] == registered_user, f"Expected email {registered_user}, got: {body['user']['email']}"
