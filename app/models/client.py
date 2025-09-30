from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

# Modelo de cliente (tabla `clients`).Representa a un cliente dentro del sistema VISE.
# Cada cliente puede estar inscrito en Vise Club y tener un tipo de tarjeta asignado.
# Además, se relaciona con la tabla `purchases` para registrar sus compras.


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    monthly_income = Column(Float, nullable=False)
    vise_club = Column(Boolean, default=False)
    card_type = Column(String, nullable=False)

    purchases = relationship("Purchase", back_populates="client")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    purchase_date = Column(DateTime, nullable=False)
    purchase_country = Column(String, nullable=False)

    client = relationship("Client", back_populates="purchases")
