from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from core.self_healing_engine import SelfHealingEngine
from core.locator_engine import update_locator

# Map locator type strings to Selenium By strategies
BY_MAP = {
    "id":    By.ID,
    "name":  By.NAME,
    "xpath": By.XPATH,
    "css":   By.CSS_SELECTOR,
    "class": By.CLASS_NAME,
}


def find_element(driver, element_name, locator, tag_type="input"):
    """
    Try to find element using stored locator.
    If it fails, trigger self-healing and retry.
    """
    by = BY_MAP.get(locator["type"], By.XPATH)

    try:
        return driver.find_element(by, locator["value"])

    except NoSuchElementException:
        print(f"⚠️  Element '{element_name}' not found. Triggering self-healing...")
        return heal(driver, element_name, tag_type)


def heal(driver, element_name, tag_type="input"):
    """
    Self-healing: scan page HTML, find best locator,
    update JSON file, and return the found element.
    """
    engine = SelfHealingEngine()
    html = driver.page_source
    new_locator = engine.find_best_locator(html, tag_type)

    update_locator(element_name, new_locator)
    print(f"✅ Healed '{element_name}' → {new_locator}")

    by = BY_MAP.get(new_locator["type"], By.XPATH)
    return driver.find_element(by, new_locator["value"])
