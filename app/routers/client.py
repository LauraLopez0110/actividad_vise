from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientLogin, Token
from app.security.hashing import hash_password
from app.security.auth import create_access_token, authenticate_client

router = APIRouter(tags=["Clients"])

@router.post("/client", response_model=ClientResponse)
def register_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing_client = db.query(Client).filter(Client.email == client.email).first()
    if existing_client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_client = Client(email=client.email, hashed_password=hash_password(client.password))
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.post("/login", response_model=Token)
def login(client_credentials: ClientLogin, db: Session = Depends(get_db)):
    client = authenticate_client(db, client_credentials.email, client_credentials.password)
    if not client:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(client.id)})
    return {"access_token": access_token, "token_type": "bearer"}
