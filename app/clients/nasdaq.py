from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
def get_nasdaq_price(symbol: str) -> float:
    url = f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")  # Скрывает автоматизацию
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")

    driver = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=options
    )
    driver.implicitly_wait(3)
    driver.get(url)
    # Get button and click it
    agree_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    agree_button.click()
    price = driver.find_element(By.CLASS_NAME, "nsdq-quote-header__info-wrapper").text.split('\n')[0][1:]
    driver.quit()
    return float(price)


