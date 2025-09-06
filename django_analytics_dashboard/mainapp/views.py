from django.shortcuts import render
import requests

API_URL = "http://localhost:8000"

def index(request):
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
        "mainapp/index.html",
        {
            "symbol": symbol,
            "start": start,
            "end": end,
            "average": analytics.get("average"),
            "history": history,
            "plot_img": plot_img
        }
    )