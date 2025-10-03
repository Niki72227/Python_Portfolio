import requests
from bs4 import BeautifulSoup

def get_ccy_investing(first_ccy, second_ccy) -> float:
    url = f"https://www.investing.com/currencies/{first_ccy}-{second_ccy}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price = float(soup.find_all('div', class_= 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')[0].text)
    return price

def get_ccy_price(first_ccy, second_ccy) -> float:
    url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={first_ccy}&To={second_ccy}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price = 0
    try:
        price_p = soup.find('p', class_='sc-c5062ab2-1 jKDFIr')
        price = float(price_p.text.split()[0])
    except:
        print("No price found")
    return price

def get_all_forex() -> list:
    url = "https://www.xe.com/symbols/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all("li", class_="sc-2c2026c5-8 Tbubm")
    tickers = []
    for i in table:
        b = i.find_all('div')
        if len(b[3].text)==3:
            tickers.append(b[3].text)
    return tickers
