import sys
import os
import pytest
from typing import Generator
from playwright.sync_api import Page

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import generate_random_email, create_user_via_api, delete_user_via_api


@pytest.fixture
def registered_user(page: Page) -> Generator[str, None, None]:
    """
    Creates a user via API before the test and deletes them after.
    Yields the generated email so the test can use it.
    """
    email = generate_random_email()
    create_user_via_api(page.request, email)
    yield email
    delete_user_via_api(page.request, email)
