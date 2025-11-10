import asyncio
import httpx
import random
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

card_types = ["Classic", "Gold", "Platinum", "Black", "White"]
countries = ["Colombia", "USA", "China", "Mexico", "Canada"]
currencies = ["USD", "COP", "EUR"]

async def register_client(client: httpx.AsyncClient, i: int):
    data = {
        "name": f"User{i}",
        "country": random.choice(countries),
        "monthlyIncome": random.randint(100, 3000),
        "viseClub": random.choice([True, False]),
        "cardType": random.choice(card_types),
    }
    r = await client.post(f"{BASE_URL}/client", json=data)
    print(f"🧍‍♂️ Client {i} -> {r.status_code}")

async def make_purchase(client: httpx.AsyncClient, i: int):
    data = {
        "clientId": random.randint(1, 5),
        "amount": round(random.uniform(50, 2000), 2),
        "currency": random.choice(currencies),
        "purchaseDate": datetime.utcnow().isoformat() + "Z",
        "purchaseCountry": random.choice(countries),
    }
    r = await client.post(f"{BASE_URL}/purchase", json=data)
    print(f"🛒 Purchase {i} -> {r.status_code}")

async def run_load_test(total_requests: int = 300):
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = []
        for i in range(total_requests):
            if random.random() < 0.5:
                tasks.append(register_client(client, i))
            else:
                tasks.append(make_purchase(client, i))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("🚀 Starting load test for FastAPI service...")
    asyncio.run(run_load_test(300))
    print("✅ Done. Check Axiom dataset (actividad-vise).")
