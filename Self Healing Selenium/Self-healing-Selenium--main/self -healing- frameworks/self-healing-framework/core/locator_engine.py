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
    """Updates locator in JSON file after self-healing."""
    with open(LOCATOR_FILE, "r") as f:
        data = json.load(f)

    data[element_name] = new_locator

    with open(LOCATOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📝 Locator updated for '{element_name}': {new_locator}")
