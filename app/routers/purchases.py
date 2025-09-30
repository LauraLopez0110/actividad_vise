from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.rules import validate_purchase, calculate_discount

"""
===========================================================
📦 Módulo: purchases.py
===========================================================

🧭 Propósito:
Gestiona las operaciones relacionadas con las compras de los clientes en el sistema VISE API.

📑 Flujo principal:
1️⃣ Verifica que el cliente exista en la base de datos.
2️⃣ Valida si la compra está permitida (por país o tipo de tarjeta).
3️⃣ Calcula el descuento aplicable y el beneficio asociado según reglas de negocio.
4️⃣ Registra la compra en la base de datos.
5️⃣ Devuelve una respuesta con los detalles de la transacción.

🔒 Validaciones:
- Los clientes con tarjetas BLACK o WHITE no pueden comprar desde países prohibidos.
- Las reglas de descuento se aplican según tipo de tarjeta, día de la semana, monto y país.

📦 Respuestas:
- 200 → Compra registrada y aprobada.
- 400 → Compra rechazada (validación o país prohibido).

===========================================================
"""

router = APIRouter(tags=["Purchases"])


@router.post(
    "/purchase",
    responses={
        200: {"model": schemas.PurchaseResponse, "description": "Compra registrada exitosamente."},
        400: {"model": schemas.PurchaseResponse, "description": "Compra rechazada por validación o país prohibido."},
    },
)
def make_purchase(data: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    """
    🛒 Registrar una nueva compra en el sistema.

    Args:
        data (schemas.PurchaseCreate): Información de la compra recibida desde el cuerpo del request.
        db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Returns:
        dict | JSONResponse:
            - Si la compra es válida → status 200 con detalle de la transacción.
            - Si es rechazada → status 400 con mensaje de error.

    Ejemplo de request:
    ```json
    {
      "clientId": 1,
      "amount": 250.75,
      "currency": "USD",
      "purchaseDate": "2025-10-06T12:00:00Z",
      "purchaseCountry": "Colombia"
    }
    ```

    Ejemplo de respuesta (200 OK):
    ```json
    {
      "status": "Approved",
      "purchase": {
        "clientId": 1,
        "originalAmount": 250.75,
        "discountApplied": 37.61,
        "finalAmount": 213.14,
        "benefit": "Sábado 30%"
      }
    }
    ```

    Ejemplo de respuesta (400 Bad Request):
    ```json
    {
      "status": "Rejected",
      "error": "El cliente con tarjeta Black no puede realizar compras desde China"
    }
    ```
    """

    # 1️⃣ Verificar existencia del cliente
    client = db.query(models.Client).filter(models.Client.id == data.clientId).first()
    if not client:
        return JSONResponse(
            status_code=400,
            content={"status": "Rejected", "error": "Cliente no encontrado"}
        )

    # 2️⃣ Validar si la compra está permitida según tipo de tarjeta y país
    ok, err = validate_purchase(client.card_type, data.purchaseCountry)
    if not ok:
        return JSONResponse(
            status_code=400,
            content={"status": "Rejected", "error": err}
        )

    # 3️⃣ Calcular descuento y beneficio según las reglas de negocio
    rate, benefit = calculate_discount(
        client.card_type,
        data.amount,
        data.purchaseDate,
        data.purchaseCountry,
        client.country
    )

    discount = round(data.amount * rate, 2)
    final = round(data.amount - discount, 2)

    # 4️⃣ Registrar la compra en la base de datos
    purchase = models.Purchase(
        client_id=client.id,
        amount=data.amount,
        currency=data.currency,
        purchase_date=data.purchaseDate,
        purchase_country=data.purchaseCountry,
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    # 5️⃣ Retornar resultado final
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
