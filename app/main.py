from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app import crud, schemas, analytics

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Crypto & Stocks & FX Dashboard API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/crypto/{symbol}", response_model=schemas.Asset, tags = ["Price"])
async def get_crypto(symbol: str, db: Session = Depends(get_db)):
    return await crud.get_crypto_price(symbol, db)

@app.get("/stock/{symbol}", response_model=schemas.Asset, tags = ["Price"])
def get_stock(symbol: str, db: Session = Depends(get_db)):
    return crud.get_stock_price(symbol, db)

@app.get("/forex/{first_ccy}_{second_ccy}", response_model=schemas.Asset, tags = ["Price"])
def get_forex(first_ccy: str,
              second_ccy: str,
              db: Session = Depends(get_db)
):
    return crud.get_forex_price(first_ccy.lower(), second_ccy.lower(), db)

@app.get("/history/{symbol}", response_model=list[schemas.History], tags = ["History"])
def get_history(
    symbol: str,
    start: str = Query(..., description="Start datetime in ISO format"),
    end: str = Query(..., description="End datetime in ISO format"),
    db: Session = Depends(get_db)
):
    return crud.get_history(symbol, start, end, db)

@app.get("/history_all", response_model=list[schemas.History], tags = ["History"])
def get_history_all(
    db: Session = Depends(get_db)
):
    return crud.get_history_all(db)

@app.get("/analytics/{symbol}", tags = ["Analytics"])
def get_analytics(
    symbol: str,
    start: str = Query(..., description="Start datetime in ISO format"),
    end: str = Query(..., description="End datetime in ISO format"),
    db: Session = Depends(get_db)
):
    return analytics.calc_average_and_plot(symbol, start, end, db)

@app.get("/crypto_symbols_all", response_model=list[schemas.All_Crypto_Symbols], tags = ["Extra"])
async def get_crypto_symbols_all(db: Session = Depends(get_db)):
    return await crud.get_all_crypto_symbols(db)

@app.get("/stock_symbols_all", response_model=list[schemas.All_Stock_Symbols], tags = ["Extra"])
def get_stock_symbols_all(db: Session = Depends(get_db)):
    return crud.get_all_stock_symbols(db)