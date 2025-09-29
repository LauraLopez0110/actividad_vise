from app.database import Base, engine
from app import models
from fastapi import FastAPI
from app.routers import clients, purchases

app = FastAPI(title="API VISE")
Base.metadata.create_all(bind=engine)

# Registrar los routers
app.include_router(clients.router)
app.include_router(purchases.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API"}