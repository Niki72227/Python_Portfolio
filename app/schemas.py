from pydantic import BaseModel
from datetime import datetime

class Asset(BaseModel):
    id: int
    type: str
    symbol: str
    price: float
    timestamp: datetime

    class Config:
        orm_mode = True

class History(BaseModel):
    id: int
    symbol: str
    price: float
    date: datetime

    class Config:
        orm_mode = True

class All_Crypto_Symbols(BaseModel):
    id: int
    symbol: str
    class Config:
        orm_mode = True

class All_Stock_Symbols(BaseModel):
    id: int
    symbol: str
    class Config:
        orm_mode = True