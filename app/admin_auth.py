import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def verify_admin(username: str, password: str) -> bool:
    """
    Verify admin login credentials.
    """

    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        return False

    return (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    )