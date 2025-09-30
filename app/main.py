from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client

app = FastAPI()

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VISE API - Clientes y Compras")

# Registrar los routers
app.include_router(client.router)
app.include_router(purchases.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API"}