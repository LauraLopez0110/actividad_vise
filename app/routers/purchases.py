from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.rules import validate_purchase, calculate_discount

"""
    Registrar una nueva compra para un cliente.

    Flujo del endpoint:
    1. Verifica que el cliente exista en la base de datos.
    2. Valida si la compra está permitida según el tipo de tarjeta y país.
    3. Calcula el descuento aplicable y el beneficio asociado.
    4. Registra la compra en la base de datos.
    5. Devuelve el resultado de la operación.
"""

router = APIRouter(tags=["Purchases"])

@router.post("/purchase", responses={200: {"model": schemas.PurchaseResponse}, 400: {"model": schemas.PurchaseResponse}})
def make_purchase(data: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    
     # Buscar cliente por ID
    client = db.query(models.Client).filter(models.Client.id == data.clientId).first()
    if not client:
        return {"status": "Rejected", "error": "Cliente no encontrado"}

    ok, err = validate_purchase(client.card_type, data.purchaseCountry)
    if not ok:
        return {"status": "Rejected", "error": err}

    rate, benefit = calculate_discount(
        client.card_type,
        data.amount,
        data.purchaseDate,
        data.purchaseCountry,
        client.country
    )
    discount = round(data.amount * rate, 2)
    final = round(data.amount - discount, 2)

    p = models.Purchase(
        client_id=client.id,
        amount=data.amount,
        currency=data.currency,
        purchase_date=data.purchaseDate,
        purchase_country=data.purchaseCountry,
    )
    db.add(p)
    db.commit()
    db.refresh(p)

    return {
        "status": "Approved",
        "purchase": {
            "clientId": client.id,
            "originalAmount": data.amount,
            "discountApplied": discount,
            "finalAmount": final,
            "benefit": benefit
        }
    }
