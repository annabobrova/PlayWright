import random
import string
from playwright.sync_api import APIRequestContext
from config import (
    BASE_URL, TEST_PASSWORD, TEST_NAME_SIGNUP,
    TEST_FIRST_NAME, TEST_LAST_NAME, TEST_COMPANY, TEST_ADDRESS,
    TEST_COUNTRY, TEST_STATE, TEST_CITY, TEST_ZIPCODE, TEST_PHONE,
    TEST_DAY, TEST_MONTH, TEST_YEAR
)

def generate_random_email() -> str:
    """
    Generates a random email address with 10 random lowercase letters
    followed by '@example.com'.
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return f"{random_string}@example.com"

def create_user_via_api(api_request_context: APIRequestContext, email: str) -> dict:
    """
    Helper function to create a user via API. 
    This can be reused in UI tests for setup.
    """
    payload = {
        "name": TEST_NAME_SIGNUP,
        "email": email,
        "password": TEST_PASSWORD,
        "title": "Mrs",
        "birth_date": TEST_DAY,
        "birth_month": TEST_MONTH,
        "birth_year": TEST_YEAR,
        "firstname": TEST_FIRST_NAME,
        "lastname": TEST_LAST_NAME,
        "company": TEST_COMPANY,
        "address1": TEST_ADDRESS,
        "address2": "Apt 101",
        "country": TEST_COUNTRY,
        "zipcode": TEST_ZIPCODE,
        "state": TEST_STATE,
        "city": TEST_CITY,
        "mobile_number": TEST_PHONE
    }
    
    # AutomationExercise API uses form data (multipart/form-data)
    response = api_request_context.post(f"{BASE_URL}/api/createAccount", form=payload)
    return response.json()

def delete_user_via_api(api_request_context: APIRequestContext, email: str) -> dict:
    """
    Helper function to delete a user via API.
    """
    delete_payload = {
        "email": email,
        "password": TEST_PASSWORD
    }
    response = api_request_context.delete(f"{BASE_URL}/api/deleteAccount", form=delete_payload)
    return response.json()
