import httpx
import requests

async def get_binance_price(symbol: str) -> float:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return float(data["price"])

async def get_all_crypto() -> list:
    url = "https://api.binance.com/api/v3/exchangeInfo?permissions=SPOT"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        symbols = [s["baseAsset"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]
        return symbols