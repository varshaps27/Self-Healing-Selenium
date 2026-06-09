from flask import Flask
from core.driver_factory import DriverFactory
from tests.test_login import test_login
import time

app = Flask(__name__)

@app.route("/")
def run_tests():
    driver = DriverFactory.get_driver()
    results = []

    try:
        results.append("🚀 Starting test run...")
        test_login(driver)
        results.append("✅ All tests passed!")
        time.sleep(3)

    except AssertionError as e:
        results.append(f"❌ TEST ASSERTION FAILED: {e}")
        time.sleep(5)

    except Exception as e:
        results.append(f"❌ TEST FAILED UNEXPECTEDLY: {e}")
        time.sleep(5)

    finally:
        driver.quit()
        results.append("🔒 Browser closed.")

    return "<br>".join(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)