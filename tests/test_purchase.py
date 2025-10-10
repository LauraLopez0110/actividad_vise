import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app

client = TestClient(app)

# ---------------------------------------------------
# ⚙️ Helpers: registrar clientes de prueba antes de comprar
# ---------------------------------------------------
def register_client(card_type, country="USA", income=3000, viseClub=True):
    """Crea un cliente válido según el tipo de tarjeta."""
    data = {
        "name": f"Cliente_{card_type}",
        "country": country,
        "monthlyIncome": income,
        "viseClub": viseClub,
        "cardType": card_type,
    }
    response = client.post("/client", json=data)
    assert response.status_code == 200, f"No se pudo registrar cliente {card_type}"
    return response.json()["clientId"]


# ---------------------------------------------------
# 🧩 Casos de prueba de beneficios y restricciones
# ---------------------------------------------------

purchase_cases = [
    # Classic → sin beneficios
    {
        "card": "Classic",
        "amount": 300,
        "weekday": 0,  # lunes
        "purchase_country": "USA",
        "expected_discount": 0.0,
    },
    # Gold → lunes-miércoles >100 → 15%
    {
        "card": "Gold",
        "amount": 150,
        "weekday": 1,  # martes
        "purchase_country": "USA",
        "expected_discount": 0.15,
    },
    # Platinum → lunes-miércoles >100 → 20%
    {
        "card": "Platinum",
        "amount": 150,
        "weekday": 2,  # miércoles
        "purchase_country": "USA",
        "expected_discount": 0.20,
    },
    # Platinum → sábado >200 → 30%
    {
        "card": "Platinum",
        "amount": 300,
        "weekday": 5,  # sábado
        "purchase_country": "USA",
        "expected_discount": 0.30,
    },
    # Platinum → exterior → 5%
    {
        "card": "Platinum",
        "amount": 150,
        "weekday": 4,  # viernes
        "purchase_country": "France",
        "expected_discount": 0.05,
    },
    # Black → lunes >100 → 25%
    {
        "card": "Black",
        "amount": 150,
        "weekday": 0,  # lunes
        "purchase_country": "USA",
        "expected_discount": 0.25,
    },
    # Black → sábado >200 → 35%
    {
        "card": "Black",
        "amount": 400,
        "weekday": 5,
        "purchase_country": "USA",
        "expected_discount": 0.35,
    },
    # Black → exterior → 5%
    {
        "card": "Black",
        "amount": 100,
        "weekday": 3,  # jueves
        "purchase_country": "France",
        "expected_discount": 0.05,
    },
    # Black → intento desde país prohibido (rechazo)
    {
        "card": "Black",
        "amount": 200,
        "weekday": 2,
        "purchase_country": "China",
        "expected_discount": None,  # rechazado
    },
    # White → lunes >100 → 25%
    {
        "card": "White",
        "amount": 150,
        "weekday": 0,
        "purchase_country": "USA",
        "expected_discount": 0.25,
    },
    # White → domingo >200 → 35%
    {
        "card": "White",
        "amount": 300,
        "weekday": 6,
        "purchase_country": "USA",
        "expected_discount": 0.35,
    },
    # White → exterior → 5%
    {
        "card": "White",
        "amount": 250,
        "weekday": 3,
        "purchase_country": "Italy",
        "expected_discount": 0.05,
    },
]


@pytest.mark.parametrize("case", purchase_cases)
def test_purchase_discounts(case):
    """Valida descuentos y restricciones de /purchase según tipo de tarjeta."""
    client_id = register_client(case["card"])

    # Genera una fecha según el día de la semana deseado
    today = datetime.utcnow()
    # ajusta weekday (0=lunes)
    delta_days = (case["weekday"] - today.weekday()) % 7
    purchase_date = today.replace(hour=12, minute=0, second=0, microsecond=0)
    purchase_date = purchase_date.fromordinal(purchase_date.toordinal() + delta_days)

    payload = {
        "clientId": client_id,
        "amount": case["amount"],
        "currency": "USD",
        "purchaseDate": purchase_date.isoformat() + "Z",
        "purchaseCountry": case["purchase_country"],
    }

    response = client.post("/purchase", json=payload)

    # Si la compra es rechazada
    if case["expected_discount"] is None:
        assert response.status_code == 400, f"Se esperaba rechazo para {case['card']}"
        body = response.json()
        assert body["status"] == "Rejected"
    else:
        assert response.status_code == 200, f"Error en {case['card']} → {response.text}"
        body = response.json()
        assert body["status"] == "Approved"
        purchase = body["purchase"]
        original = case["amount"]
        expected_final = round(original * (1 - case["expected_discount"]), 2)
        # margen de tolerancia
        assert abs(purchase["finalAmount"] - expected_final) < 0.01, f"{case['card']} descuento incorrecto"
