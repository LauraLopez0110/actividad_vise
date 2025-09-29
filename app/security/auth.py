# app/security/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

# Claves para JWT (puedes moverlas a tu config más tarde)
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función de ejemplo para “autenticar” un cliente
def authenticate_client(username: str, password: str):
    # Para pruebas: acepta cualquier usuario que no esté vacío
    if username and password:
        return {"username": username}
    return None
