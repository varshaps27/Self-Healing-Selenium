from core.driver_factory import DriverFactory
from tests.test_login import test_login


def run():
    driver = DriverFactory.get_driver()

    try:
        print("🚀 Starting test run...")
        test_login(driver)
        print("✅ All tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    run()
