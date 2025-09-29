from fastapi import FastAPI
from app.routers import client
from app.db import Base, engine

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VISE API - Clientes y Compras")

# Routers
app.include_router(client.router)
