import json
from core.config import LOCATOR_FILE

# Default credentials for reset
DEFAULT_CREDENTIALS = {
    "username": "Admin",
    "password": "admin123"
}


def get_locator(element_name):
    """Returns locator dict: { 'type': 'name', 'value': 'username' }"""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    if element_name not in data:
        raise KeyError(f"Locator '{element_name}' not found in {LOCATOR_FILE}")

    return data[element_name]


def update_locator(element_name, new_locator):
    """Updates locator in JSON file after self-healing."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    data[element_name] = new_locator

    with open(LOCATOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📝 Locator updated for '{element_name}': {new_locator}")


def get_credentials():
    """Returns credentials dict: { 'username': 'Admin', 'password': 'admin123' }"""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    if "credentials" not in data:
        raise KeyError(f"Credentials not found in {LOCATOR_FILE}")

    return data["credentials"]


def reset_credentials():
    """Resets credentials to default values in JSON file."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    data["credentials"] = DEFAULT_CREDENTIALS

    with open(LOCATOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"🔄 Credentials reset to default: {DEFAULT_CREDENTIALS['username']}")
