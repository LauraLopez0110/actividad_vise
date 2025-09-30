from pydantic import BaseModel, Field
from datetime import datetime
from app.rules import CardType

"""
    Esquema de entrada para registrar un nuevo cliente.
    
    Campos:
    - name → Nombre completo del cliente.
    - country → País de residencia.
    - monthlyIncome → Ingreso mensual declarado.
    - viseClub → Indica si pertenece al VISE CLUB.
    - cardType → Tipo de tarjeta solicitada (usa Enum CardType).
    """

# ---------- CLIENTES ----------
class ClientCreate(BaseModel):
    name: str = Field(..., example="Alice Classic")
    country: str = Field(..., example="USA")
    monthlyIncome: float = Field(..., example=1000.50)
    viseClub: bool = Field(..., example=False)
    cardType: CardType = Field(..., example="Classic")  # Enum, pero ejemplo como string

class ClientResponse(BaseModel):
    clientId: int = Field(..., example=1)
    name: str = Field(..., example="Alice Classic")
    cardType: CardType = Field(..., example="Classic")
    status: str = Field(..., example="Registered")
    message: str = Field(..., example="Client registered successfully")

    class Config:
        orm_mode = True

class ClientErrorResponse(BaseModel):
    status: str = Field(..., example="Rejected")
    error: str = Field(..., example="Monthly income too low for selected card")


# ---------- COMPRAS ----------
class PurchaseCreate(BaseModel):
    clientId: int = Field(..., example=1)
    amount: float = Field(..., example=250.75)
    currency: str = Field(..., example="USD")
    purchaseDate: datetime = Field(..., example="2025-09-29T12:00:00Z")
    purchaseCountry: str = Field(..., example="Colombia")

class PurchaseResponse(BaseModel):
    status: str = Field(..., example="Success")
    purchase: dict | None = Field(
        default=None,
        example={
            "id": 101,
            "clientId": 1,
            "amount": 250.75,
            "currency": "USD",
            "purchaseDate": "2025-09-29T12:00:00Z",
            "purchaseCountry": "Colombia"
        }
    )
    error: str | None = Field(default=None, example=None)
