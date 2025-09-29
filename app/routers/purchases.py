# app/routers/purchases.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.rules import validate_purchase, calculate_discount

router = APIRouter(prefix="/purchase", tags=["Purchases"])

@router.post("/", responses={200: {"model": schemas.PurchaseResponse}, 400: {"model": schemas.PurchaseResponse}})

def make_purchase(data: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == data.clientId).first()
    if not client:
        return {"status": "Rejected", "error": "Cliente no encontrado"}

    ok, err = validate_purchase(client.card_type, data.purchaseCountry)
    if not ok:
        return {"status": "Rejected", "error": err}

    rate, benefit = calculate_discount(client.card_type, data.amount, data.purchaseDate, data.purchaseCountry, client.country)
    discount = round(data.amount * rate, 2)
    final = round(data.amount - discount, 2)

    p = models.Purchase(
        client_id=client.id,
        amount=data.amount,
        currency=data.currency,
        purchase_date=data.purchaseDate,
        purchase_country=data.purchaseCountry,
    )
    db.add(p); db.commit(); db.refresh(p)

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
