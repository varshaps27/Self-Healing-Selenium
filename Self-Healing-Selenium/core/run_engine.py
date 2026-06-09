import time
from core.driver_factory import DriverFactory
from tests.test_login import test_login


def run():
    driver = DriverFactory.get_driver()

    try:
        print("🚀 Starting test run...")
        test_login(driver)
        print("✅ All tests passed!")
        time.sleep(3)

    except AssertionError as e:
        print(f"❌ TEST ASSERTION FAILED: {e}")
        time.sleep(5)

    except Exception as e:
        print(f"❌ TEST FAILED UNEXPECTEDLY: {e}")
        time.sleep(5)

    finally:
        driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    run()
