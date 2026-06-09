from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from core.self_healing_engine import SelfHealingEngine
from core.locator_engine import update_locator

BY_MAP = {
    "id":    By.ID,
    "name":  By.NAME,
    "xpath": By.XPATH,
    "css":   By.CSS_SELECTOR,
    "class": By.CLASS_NAME,
}

WAIT_TIMEOUT = 20


def find_element(driver, element_name, locator, tag_type="input"):
    """
    Waits for element to be visible and clickable.
    Triggers self-healing if not found within timeout.
    """
    by = BY_MAP.get(locator["type"], By.XPATH)

    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((by, locator["value"]))
        )
        element = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((by, locator["value"]))
        )
        return element

    except (TimeoutException, ElementNotInteractableException):
        print(f"⚠️  Element '{element_name}' not interactable. Triggering self-healing...")
        return heal(driver, element_name, tag_type)


def heal(driver, element_name, tag_type="input"):
    """
    Self-healing: scan HTML, find best locator, update JSON, return element.
    """
    engine = SelfHealingEngine()
    html = driver.page_source
    new_locator = engine.find_best_locator(html, tag_type)

    update_locator(element_name, new_locator)
    print(f"✅ Healed '{element_name}' → {new_locator}")

    by = BY_MAP.get(new_locator["type"], By.XPATH)

    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((by, new_locator["value"]))
    )
    return element
