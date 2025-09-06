from sqlalchemy.orm import Session
from app.models import Asset, History
from datetime import datetime
from app.clients.binance import get_binance_price
from app.clients.nasdaq import get_nasdaq_price
from app.clients.forex import get_ccy

async def get_crypto_price(symbol: str, db: Session):
    price = await get_binance_price(symbol)
    asset = Asset(type="crypto", symbol=symbol, price=price, timestamp=datetime.utcnow())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    history = History(symbol=symbol, price=price, date=datetime.utcnow())
    db.add(history)
    db.commit()
    return asset

def get_stock_price(symbol: str, db: Session):
    price = get_nasdaq_price(symbol)
    asset = Asset(type="stock", symbol=symbol, price=price, timestamp=datetime.utcnow())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    history = History(symbol=symbol, price=price, date=datetime.utcnow())
    db.add(history)
    db.commit()
    return asset

def get_forex_price(first_ccy:str, second_ccy:str, db: Session):
    price = get_ccy(first_ccy, second_ccy)
    asset = Asset(type="forex", symbol=f"{first_ccy.upper()}/{second_ccy.upper()}", price=price, timestamp=datetime.utcnow())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    history = History(symbol=f"{first_ccy.upper()}/{second_ccy.upper()}", price=price, date=datetime.utcnow())
    db.add(history)
    db.commit()
    return asset

def get_history(symbol: str, start: str, end: str, db: Session):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    return db.query(History).filter(
        History.symbol == symbol,
        History.date >= start_dt,
        History.date <= end_dt
    ).all()