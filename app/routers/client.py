from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Client
from app.schemas import ClientCreate, ClientResponse
from typing import List

# Participación de [Persona 1]: implementación de los endpoints relacionados con clientes

router = APIRouter(prefix="/clients", tags=["clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear cliente
@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Validar que el email no exista
    existing = db.query(Client).filter(Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_client = Client(name=client.name, email=client.email, password=client.password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Listar todos los clientes
@router.get("/", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients

# Obtener un cliente por ID
@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client
