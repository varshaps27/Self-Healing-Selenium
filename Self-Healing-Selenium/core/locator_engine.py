import json
from core.config import LOCATOR_FILE


def get_locator(element_name):
    """Returns locator dict: { 'type': 'name', 'value': 'username' }"""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    if element_name not in data:
        raise KeyError(f"Locator '{element_name}' not found in {LOCATOR_FILE}")

    return data[element_name]


def update_locator(element_name, new_locator):
    """Overwrites a locator in the JSON file after self-healing."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    data[element_name] = new_locator

    with open(LOCATOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📝 Locator updated for '{element_name}': {new_locator}")


def get_credentials():
    """Returns stored credentials from the JSON file."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    return data.get("credentials", {"username": "Admin", "password": "admin123"})


def reset_credentials():
    """Resets credentials back to default values after a failed login."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    data["credentials"] = {
        "username": "Admin",
        "password": "admin123"
    }

    with open(LOCATOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("🔧 Credentials auto-reset to default values.")
