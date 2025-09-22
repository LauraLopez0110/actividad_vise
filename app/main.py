from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client, purchases

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VISE API - Clientes y Compras")

# Registrar routers
app.include_router(client.router)
app.include_router(purchases.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API"}
