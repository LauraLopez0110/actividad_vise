
from datetime import datetime
from enum import Enum

BANNED_COUNTRIES = {"China", "Vietnam", "India", "Irán"}

class CardType(str, Enum):
    CLASSIC = "Classic"
    GOLD    = "Gold"
    PLAT    = "Platinum"
    BLACK   = "Black"
    WHITE   = "White"

def validate_client(card_type: str, income: float, vise_club: bool, country: str) -> tuple[bool, str]:
    if card_type == CardType.GOLD and income < 500:
        return False, "El cliente no cumple con el ingreso mínimo de 500 USD para Gold"
    if card_type == CardType.PLAT:
        if income < 1000:
            return False, "El cliente no cumple con el ingreso mínimo de 1000 USD para Platinum"
        if not vise_club:
            return False, "El cliente no cumple con la suscripción VISE CLUB requerida para Platinum"
    if card_type in (CardType.BLACK, CardType.WHITE):
        if income < 2000:
            return False, "El cliente no cumple con el ingreso mínimo de 2000 USD"
        if not vise_club:
            return False, "El cliente no cumple con la suscripción VISE CLUB requerida"
        if country in BANNED_COUNTRIES:
            return False, f"El cliente con tarjeta {card_type} no puede residir en {country}"
    return True, "Cliente apto"

def validate_purchase(card_type: str, purchase_country: str) -> tuple[bool, str | None]:
    if card_type in (CardType.BLACK, CardType.WHITE) and purchase_country in BANNED_COUNTRIES:
        return False, f"El cliente con tarjeta {card_type} no puede realizar compras desde {purchase_country}"
    return True, None

def calculate_discount(card_type: str, amount: float, date: datetime, purchase_country: str, client_country: str) -> tuple[float, str | None]:
    wd = date.weekday()  #  convertimos la fecha en numero 0=lunes 1 = martes 2 = miercoles 3 jueves 4  viernes 5 sabado ,6=domingo
   # no tiene descuento
    if card_type == CardType.CLASSIC:
        return 0.0, None
    
    if card_type == CardType.GOLD:
        if wd in (0,1,2) and amount > 100:
            return 0.15, "Lunes - Miércoles 15%"

    elif card_type == CardType.PLAT:
        if wd in (0,1,2) and amount > 100:
            return 0.20, "Lunes - Miércoles 20%"
        
        if wd == 5 and amount > 200:
            return 0.30, "Sábado 30%"
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"

    elif card_type == CardType.BLACK:
        if wd in (0,1,2) and amount > 100:
            return 0.25, "Lunes - Miércoles 25%"
        if wd == 5 and amount > 200:
            return 0.35, "Sábado 35%"
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"

    elif card_type == CardType.WHITE:
        if wd in (0,1,2,3,4) and amount > 100:
            return 0.25, "Lunes - Viernes 25%"
        if wd in (5,6) and amount > 200:
            return 0.35, "Fin de semana 35%"
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"

    return 0.0, None
