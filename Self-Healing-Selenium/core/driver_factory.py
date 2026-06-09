import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class DriverFactory:

    @staticmethod
    def get_driver():
        options = Options()

        # ── Required for server/cloud deployment (Render, Heroku etc.) ──
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # ── Detect if running on Render/Linux server ──────────────────
        chrome_bin = os.environ.get("GOOGLE_CHROME_BIN") or os.environ.get("CHROME_BIN")
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

        if chrome_bin:
            options.binary_location = chrome_bin

        if chromedriver_path:
            # Running on Render — use installed chromedriver path
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            # Running locally — Selenium 4.6+ manages driver automatically
            driver = webdriver.Chrome(options=options)

        return driver
