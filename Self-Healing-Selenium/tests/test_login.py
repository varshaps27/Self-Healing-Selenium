import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from core.config import BASE_URL
from core.locator_engine import get_locator, get_credentials, reset_credentials
from core.element_actions import find_element

MAX_RETRIES = 2


def test_login(driver):

    # ── STEP 1: Open login page ─────────────────────────────────────
    print("🌐 Opening OrangeHRM login page...")
    driver.get(BASE_URL)

    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        print("✅ Page loaded successfully.")
    except TimeoutException:
        raise Exception("❌ Login page did not load within 30 seconds.")

    # ── STEP 2: Load locators ───────────────────────────────────────
    username_locator = get_locator("username")
    password_locator = get_locator("password")
    button_locator   = get_locator("login_button")

    # ── STEP 3: Retry loop with self-healing ────────────────────────
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n🔄 Login attempt {attempt} of {MAX_RETRIES}...")

        creds        = get_credentials()
        username_val = creds["username"]
        password_val = creds["password"]

        # Enter username
        try:
            field = find_element(driver, "username", username_locator, tag_type="input")
            field.clear()
            field.send_keys(username_val)
            print(f"✅ Username entered: {username_val}")
        except Exception as e:
            raise Exception(f"❌ Failed to enter username: {e}")

        time.sleep(1)

        # Enter password
        try:
            field = find_element(driver, "password", password_locator, tag_type="input")
            field.clear()
            field.send_keys(password_val)
            print("✅ Password entered.")
        except Exception as e:
            raise Exception(f"❌ Failed to enter password: {e}")

        time.sleep(1)

        # Click login button
        try:
            find_element(driver, "login_button", button_locator, tag_type="button").click()
            print("✅ Login button clicked.")
        except Exception as e:
            raise Exception(f"❌ Failed to click login button: {e}")

        time.sleep(3)

        # ── STEP 4: Check for error message ─────────────────────────
        try:
            error_el = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-alert-content-text"))
            )
            error_text = error_el.text
            print(f"⚠️  Login error detected: '{error_text}'")

            if attempt < MAX_RETRIES:
                print("🔧 Auto-healing credentials back to default...")
                reset_credentials()
                driver.get(BASE_URL)
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.NAME, "username"))
                )
                continue
            else:
                raise AssertionError(
                    f"❌ Login failed after {MAX_RETRIES} attempts: '{error_text}'"
                )

        except TimeoutException:
            pass  # No error shown — good

        # ── STEP 5: Confirm dashboard loaded ─────────────────────────
        try:
            WebDriverWait(driver, 60).until(
                EC.any_of(
                    EC.url_contains("dashboard"),
                    EC.url_contains("viewPersonalDetails"),
                    EC.presence_of_element_located((By.CLASS_NAME, "oxd-topbar-header"))
                )
            )
            print("✅ Login action completed. Dashboard loaded!")
            return

        except TimeoutException:
            current_url = driver.current_url
            if attempt < MAX_RETRIES:
                print(f"⚠️  Dashboard not loaded (URL: {current_url}). Retrying...")
                reset_credentials()
                driver.get(BASE_URL)
                continue
            else:
                raise AssertionError(
                    f"❌ Dashboard did not load after {MAX_RETRIES} attempts.\n"
                    f"   Current URL: {current_url}"
                )
