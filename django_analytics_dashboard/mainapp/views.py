from django.shortcuts import render
import requests
from django.http import JsonResponse
import datetime

API_URL = "http://localhost:8000"

def index(request):
    context = {}
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
    symbol = request.GET.get("symbol", "")
    start = request.GET.get("start", "2025-09-01T00:00")
    end = request.GET.get("end", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"))

    return render(
        request,
        "mainapp/queries.html",
        {
            "symbol": symbol,
            "start": start,
            "end": end,
        },
    )

def asset_stats(request):
    symbol = request.GET.get("q", "").split(',')[0]
    start = request.GET.get("q", "").split(',')[1]
    end = request.GET.get("q", "").split(',')[2]
    analytics = requests.get(f"{API_URL}/analytics/{symbol.lower()}", params={"start": start, "end": end}).json()
    history = requests.get(f"{API_URL}/history/{symbol.lower()}", params={"start": start, "end": end}).json()

    plot_img = None
    if analytics.get("plot"):
        plot_img = f"data:image/png;base64,{analytics['plot']}"

    return JsonResponse({
            "average": analytics.get("average"),
            "history": history,
            "plot_img": plot_img
        })


def get_crypto_list(request):
    cs_all_json = requests.get(f"{API_URL}/crypto_symbols_all").json()
    crypto_symbols = [entry["symbol"] for entry in cs_all_json]
    query = request.GET.get("q", "").upper()
    results = [s for s in crypto_symbols if query in s] if query else []
    return JsonResponse({"results": results})

def get_stock_list(request):
    ss_all_json = requests.get(f"{API_URL}/stock_symbols_all").json()
    stock_symbols = [entry["symbol"] for entry in ss_all_json]
    query = request.GET.get("q", "").upper()
    results = [s for s in stock_symbols if query in s] if query else []
    return JsonResponse({"results": results})

def get_ccy_list(request):
    fs_all_json = requests.get(f"{API_URL}/forex_symbols_all").json()
    forex_symbols = [entry["symbol"] for entry in fs_all_json]
    query = request.GET.get("q", "").upper()
    results = [s for s in forex_symbols if query in s] if query else []
    return JsonResponse({"results": results})

def get_crypto_price(request):
    symbol = request.GET.get("q", "").upper()
    price = requests.get(f"{API_URL}/crypto/{symbol}").json()
    results = price["price"]
    return JsonResponse({"results": results})

def get_stock_price(request):
    symbol = request.GET.get("q", "").upper()
    price = requests.get(f"{API_URL}/stock/{symbol}").json()
    results = price["price"]
    return JsonResponse({"results": results})

def get_ccy_price(request):
    first_ccy = request.GET.get("q", "").upper().split(',')[0]
    second_ccy = request.GET.get("q", "").upper().split(',')[1]
    price = requests.get(f"{API_URL}/forex/{first_ccy}_{second_ccy}").json()
    results = price["price"]
    return JsonResponse({"results": results})

def get_asset_list(request):
    asset_list = requests.get(f"{API_URL}/assets_all").json()
    result = [asset["symbol"].upper() for asset in asset_list]
    result = sorted(set(result))
    query = request.GET.get("q", "").upper()
    results = [s for s in result if query in s] if query else []
    return JsonResponse({"results": results})