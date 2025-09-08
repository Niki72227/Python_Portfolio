from django.shortcuts import render
import requests

API_URL = "http://localhost:8000"

def index(request):
    context = {}
    if request.method == "GET":
        action = request.GET.get('action')
        if action == 'crypto':
            symbol = request.GET.get("crypto_symbol", "BTC")
            try:
                price = requests.get(f"{API_URL}/crypto/{symbol.lower()}").json()['price']
            except:
                price = "Invalid Crypto Symbol"
            context = {"crypto_symbol": symbol.upper(), "price_crypto": price}
        elif action == 'stock':
            symbol = request.GET.get("stock_symbol", "AAPL")
            try:
                price = requests.get(f"{API_URL}/stock/{symbol.upper()}").json()['price']
            except:
                price = "Invalid Stock Symbol"
            context = {"stock_symbol": symbol.upper(), "price_stock": price}
        elif action == 'forex':
            first_currency = request.GET.get("first_currency", "USD")
            second_currency = request.GET.get("second_currency", "EUR")
            try:
                price = requests.get(f"{API_URL}/forex/{first_currency}_{second_currency}").json()["price"]
            except:
                price = "Invalid Currency Symbols"
            context = {"first_currency": first_currency.upper(), "second_currency": second_currency.upper(), "price_forex": price}
        else:
            price = "invalid form"
    return render(
        request,
            template_name = "mainapp/index.html",
            context= context,
    )


def history(request):
    history = requests.get(f"{API_URL}/history_all").json()
    return render(
        request,
        "mainapp/history.html",
        {"history": history}
    )

def queries(request):
    symbol = request.GET.get("symbol", "BTC")
    start = request.GET.get("start", "2025-09-01T00:00:00")
    end = request.GET.get("end", "2025-09-05T23:59:59")

    analytics = requests.get(f"{API_URL}/analytics/{symbol.lower()}", params={"start": start, "end": end}).json()
    history = requests.get(f"{API_URL}/history/{symbol.lower()}", params={"start": start, "end": end}).json()

    plot_img = None
    if analytics.get("plot"):
        plot_img = f"data:image/png;base64,{analytics['plot']}"

    return render(
        request,
        "mainapp/queries.html",
        {
            "symbol": symbol,
            "start": start,
            "end": end,
            "average": analytics.get("average"),
            "history": history,
            "plot_img": plot_img
        },
    )