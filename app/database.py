import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# URL de la base de datos
# Si no existe en las variables de entorno, usa SQLite por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vise_db.db")

# Crear el motor de base de datos
# - Para SQLite se requiere el parámetro "check_same_thread" para evitar errores de concurrencia
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

"""
    Provee una sesión de base de datos para usar en dependencias de FastAPI.
    
    - Se inyecta en endpoints con `Depends(get_db)`.
    - Maneja apertura y cierre de sesión automáticamente.

"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
