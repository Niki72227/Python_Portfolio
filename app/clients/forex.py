import requests
from bs4 import BeautifulSoup

def get_ccy(first_ccy, second_ccy) -> float:
    url = f"https://www.investing.com/currencies/{first_ccy}-{second_ccy}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price = float(soup.find_all('div', class_= 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')[0].text)
    return price
