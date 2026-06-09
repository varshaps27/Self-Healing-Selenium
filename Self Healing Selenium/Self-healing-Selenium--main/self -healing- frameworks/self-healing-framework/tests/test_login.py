from core.config import BASE_URL
from core.locator_engine import get_locator
from core.element_actions import find_element


def test_login(driver):
    driver.get(BASE_URL)

    username_locator = get_locator("username")
    password_locator = get_locator("password")
    button_locator   = get_locator("login_button")

    find_element(driver, "username",     username_locator,  tag_type="input").send_keys("Admin")
    find_element(driver, "password",     password_locator,  tag_type="input").send_keys("admin123")
    find_element(driver, "login_button", button_locator,    tag_type="button").click()

    print("✅ Login action completed.")
