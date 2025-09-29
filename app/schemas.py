from pydantic import BaseModel
from datetime import datetime
from app.rules import CardType 

## ---------- CLIENTES ----------
class ClientCreate(BaseModel):
    name: str
    country: str
    monthlyIncome: float
    viseClub: bool
    cardType: CardType  
class ClientResponse(BaseModel):
    clientId: int
    name: str
    cardType: CardType  
    status: str
    message: str

    class Config:
        orm_mode = True

class ClientErrorResponse(BaseModel):
    status: str
    error: str


# ---------- COMPRAS ----------
class PurchaseCreate(BaseModel):
    clientId: int
    amount: float
    currency: str
    purchaseDate: datetime
    purchaseCountry: str

class PurchaseResponse(BaseModel):
    status: str
    purchase: dict | None = None
    error: str | None = None