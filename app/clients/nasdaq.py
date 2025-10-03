import pandas
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd
from io import StringIO
def get_nasdaq_price(symbol: str) -> float:
    url = f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")  # Скрывает автоматизацию
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")

    driver = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=options
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.implicitly_wait(3)
    driver.get(url)
    price = float()
    # Get button and click it
    try:
        agree_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        agree_button.click()
    except:
        print("no agree_button found")
    try:
        price = driver.find_element(By.CLASS_NAME, "nsdq-quote-header__info-wrapper").text.split('\n')[0][1:]
    except:
        print("no price found")
    driver.quit()
    return price

def get_all_stocks() -> list:
    url = "https://www.nasdaq.com/market-activity/stocks/screener?page=1&rows_per_page=10000"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")  # Скрывает автоматизацию
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")

    # Настройки для автоматической загрузки
    download_dir = "/downloads"

    prefs = {
        "download.default_directory": download_dir,  # Папка для загрузки
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=options,
    )
    driver.implicitly_wait(5)
    driver.get(url)
    # Get button and click it
    try:
        agree_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        agree_button.click()
    except:
        print("no agree_button found")

    df = []
    # Download CSV file
    try:
        StockData = driver.find_element(By.CLASS_NAME, "jupiter22-c-symbol-screener-table").get_attribute('outerHTML')
        with open("table.html", "w", encoding="utf-8") as f:
            f.write(StockData)
        with open("table.html", "r", encoding="utf-8") as f:
            table_html = f.read()
        df = pd.read_html(StringIO(table_html))[0]['Symbol'].tolist()
    except:
        print("no df found")
    driver.quit()

    return df
