from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "crypto", "stock", "forex"
    symbol = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

class All_Crypto_Symbols(Base):
    __tablename__ = "all_crypto_symbols"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)