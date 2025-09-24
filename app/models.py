from sqlalchemy import Column, Integer, String
from .database import Base

# Participación de [Persona 2]: definición del modelo de Cliente
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
