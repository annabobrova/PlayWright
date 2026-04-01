import os

# Test Configuration Constants

# User Registration Data
TEST_PASSWORD = "password"
TEST_FIRST_NAME = "Anna"
TEST_LAST_NAME = "Bobrova"
TEST_COMPANY = ""
TEST_ADDRESS = "5 Barney Hill rd"
TEST_ADDRESS_2 = "Apt 101"
TEST_COUNTRY = "United States"
TEST_STATE = "NY"
TEST_CITY = "New York"
TEST_ZIPCODE = "01234"
TEST_PHONE = "12345678324"
TEST_SEARCH_PRODUCT = "Winter Top"
TEST_NAME_SIGNUP = "Anna"

# Date of Birth
TEST_DAY = "7"
TEST_MONTH = "7"
TEST_YEAR = "1975"

# Base URL
BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com/")

# Login fixture credentials
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "playwright@automationexercise.com")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "Password123!")

