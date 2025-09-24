from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client

app = FastAPI()

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(client.router)
