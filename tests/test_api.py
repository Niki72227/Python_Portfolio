import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_crypto():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/crypto/BTC")
        assert response.status_code == 200
        assert "price" in response.json()

def test_get_stock():
    # Аналогично для акций
    pass