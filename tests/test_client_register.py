import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- Datos de entrada por tipo de tarjeta ---
clients_data = [
    # Classic → sin restricciones
    {"name": "Alice Classic", "country": "USA", "monthlyIncome": 300, "viseClub": False, "cardType": "Classic", "expected_status": 200},

    # Gold → ingreso >= 500
    {"name": "Bob Gold", "country": "USA", "monthlyIncome": 400, "viseClub": False, "cardType": "Gold", "expected_status": 400},
    {"name": "Carol Gold", "country": "USA", "monthlyIncome": 700, "viseClub": False, "cardType": "Gold", "expected_status": 200},

    # Platinum → ingreso >= 1000 y VISE CLUB
    {"name": "Dan Platinum", "country": "USA", "monthlyIncome": 900, "viseClub": True, "cardType": "Platinum", "expected_status": 400},
    {"name": "Eve Platinum", "country": "USA", "monthlyIncome": 1200, "viseClub": False, "cardType": "Platinum", "expected_status": 400},
    {"name": "Frank Platinum", "country": "USA", "monthlyIncome": 1500, "viseClub": True, "cardType": "Platinum", "expected_status": 200},

    # Black → ingreso >= 2000, VISE CLUB y no país prohibido
    {"name": "Grace Black", "country": "USA", "monthlyIncome": 2500, "viseClub": True, "cardType": "Black", "expected_status": 200},
    {"name": "Hank Black", "country": "China", "monthlyIncome": 3000, "viseClub": True, "cardType": "Black", "expected_status": 400},
    {"name": "Ivan Black", "country": "USA", "monthlyIncome": 1500, "viseClub": True, "cardType": "Black", "expected_status": 400},
    {"name": "Judy Black", "country": "USA", "monthlyIncome": 2500, "viseClub": False, "cardType": "Black", "expected_status": 400},

    # White → mismas reglas que Black
    {"name": "Ken White", "country": "USA", "monthlyIncome": 2500, "viseClub": True, "cardType": "White", "expected_status": 200},
    {"name": "Lara White", "country": "Vietnam", "monthlyIncome": 2500, "viseClub": True, "cardType": "White", "expected_status": 400},
]


@pytest.mark.parametrize("data", clients_data)
def test_register_client(data):
    """Verifica que el endpoint /client respete las restricciones de cada tarjeta."""
    response = client.post("/client", json={
        "name": data["name"],
        "country": data["country"],
        "monthlyIncome": data["monthlyIncome"],
        "viseClub": data["viseClub"],
        "cardType": data["cardType"],
    })

    if data["expected_status"] == 200:
        assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}: {response.text}"
        body = response.json()
        assert body["status"] == "Registered"
        assert body["cardType"] == data["cardType"]
    else:
        assert response.status_code in (400, 422, 500), f"Esperado error, recibido {response.status_code}"
        body = response.json()
        assert body["status"] == "Rejected" or "error" in body
