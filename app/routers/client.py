# app/routers/clients.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.rules import validate_client

router = APIRouter(prefix="/client", tags=["Clients"])

@router.post("/", responses={200: {"model": schemas.ClientResponse}, 400: {"model": schemas.ClientErrorResponse}})

def register_client(data: schemas.ClientCreate, db: Session = Depends(get_db)):
    ok, msg = validate_client(data.cardType, data.monthlyIncome, data.viseClub, data.country)
    if not ok:
        return JSONResponse(status_code=400, content={"status": "Rejected", "error": msg})

    c = models.Client(
        name=data.name,
        country=data.country,
        monthly_income=data.monthlyIncome,
        vise_club=data.viseClub,
        card_type=data.cardType.value if hasattr(data.cardType, "value") else data.cardType
    )
    db.add(c); db.commit(); db.refresh(c)
    return {"clientId": c.id, "name": c.name, "cardType": c.card_type, "status": "Registered", "message": msg}
