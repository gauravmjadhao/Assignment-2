

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --------- CONFIG ----------
# Put test credentials here OR set environment variables TEST_GMAIL_EMAIL and TEST_GMAIL_PASSWORD
EMAIL = os.environ.get("TEST_GMAIL_EMAIL", "gaurav.jadhav441@gmail.com")
PASSWORD = os.environ.get("TEST_GMAIL_PASSWORD", "your_password_here")
# --------------------------

def main():
    options = Options()
    options.add_argument("--start-maximized")
    # Do NOT use headless mode for login attempts — Google detects headless more easily.
    # options.add_argument("--headless=new")  # <-- don't enable for this purpose

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://accounts.google.com/ServiceLogin?service=mail")
        print("Opened Gmail login page.")
        # Wait for email input
        email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.clear()
        email_input.send_keys(EMAIL)
        time.sleep(0.5)

        # Click identifierNext
        next_btn = driver.find_element(By.ID, "identifierNext")
        next_btn.click()
        print("Clicked Next after email.")

        # Wait for password field to appear
        # Google sometimes uses iframe or dynamic fields; wait for typical selectors
        password_locator = (By.NAME, "password")
        try:
            password_input = wait.until(EC.presence_of_element_located(password_locator))
        except Exception:
            # Sometimes Google shows another interstitial — try a longer wait
            password_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located(password_locator))

        time.sleep(0.5)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        time.sleep(0.5)

        # Click password Next button
        # The button can have ID 'passwordNext'
        try:
            pwd_next = driver.find_element(By.ID, "passwordNext")
            pwd_next.click()
            print("Clicked Next after password.")
        except Exception:
            # fallback: try to submit form via ENTER
            from selenium.webdriver.common.keys import Keys
            password_input.send_keys(Keys.RETURN)
            print("Submitted password via ENTER fallback.")

        # Wait a little for any redirect / response
        time.sleep(5)

        # Print results for debugging
        current_url = driver.current_url
        print("Current URL after attempt:", current_url)

        # Print a short snippet of page text to inspect messages (like CAPTCHA / blocked)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        snippet = body_text[:1000]  # first 1000 chars
        print("Page text snippet (first 1000 chars):")
        print(snippet)

        # Leave browser open so you can interact manually if desired
        input("Press Enter to close browser and exit...")

    except Exception as e:
        print("Exception occurred:", repr(e))
        input("Press Enter to close browser and exit...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
