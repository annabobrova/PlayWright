import random
import string

def generate_random_email() -> str:
    """
    Generates a random email address with 10 random lowercase letters
    followed by '@example.com'.
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return f"{random_string}@example.com"
