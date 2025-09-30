from datetime import datetime
from enum import Enum

# ============================================================
# 🌍 Lista de países prohibidos
# ============================================================
BANNED_COUNTRIES = {"China", "Vietnam", "India", "Irán"}

"""
===========================================================
🏦 Tipos de tarjeta disponibles en el sistema
===========================================================

- Classic  → Sin beneficios adicionales.
- Gold     → Beneficios medios (requiere ingresos mínimos).
- Platinum → Beneficios altos (requiere ingresos y membresía VISE CLUB).
- Black    → Beneficios premium (con restricciones).
- White    → Máximo nivel de beneficios (con restricciones).
"""
class CardType(str, Enum):
    CLASSIC = "Classic"
    GOLD    = "Gold"
    PLAT    = "Platinum"
    BLACK   = "Black"
    WHITE   = "White"


# ============================================================
# 👤 Validación de clientes
# ============================================================

def validate_client(card_type: str, income: float, vise_club: bool, country: str) -> tuple[bool, str]:
    """
    Valida si un cliente cumple los requisitos para registrarse con un tipo de tarjeta.

    Reglas:
    - Gold → Ingreso mínimo 500 USD.
    - Platinum → Ingreso mínimo 1000 USD y pertenencia a VISE CLUB.
    - Black/White → Ingreso mínimo 2000 USD, pertenencia a VISE CLUB y no residir en países prohibidos.

    Args:
        card_type (str): Tipo de tarjeta solicitada.
        income (float): Ingreso mensual declarado.
        vise_club (bool): Indica si pertenece al VISE CLUB.
        country (str): País de residencia.

    Returns:
        (bool, str): Resultado de validación y mensaje asociado.
    """
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


# ============================================================
# 🌐 Validación de compras
# ============================================================

def validate_purchase(card_type: str, purchase_country: str) -> tuple[bool, str | None]:
    """
    Valida si un cliente puede realizar una compra en un país específico.

    Reglas:
    - Clientes con tarjeta Black o White no pueden comprar desde países prohibidos.

    Args:
        card_type (str): Tipo de tarjeta del cliente.
        purchase_country (str): País donde se intenta realizar la compra.

    Returns:
        (bool, str | None): Resultado de validación y mensaje de error (si aplica).
    """
    if card_type in (CardType.BLACK, CardType.WHITE) and purchase_country in BANNED_COUNTRIES:
        return False, f"El cliente con tarjeta {card_type} no puede realizar compras desde {purchase_country}"
    return True, None


# ============================================================
# 💸 Cálculo de descuentos
# ============================================================

def calculate_discount(card_type: str, amount: float, date: datetime, purchase_country: str, client_country: str) -> tuple[float, str | None]:
    """
    Calcula el descuento aplicable a una compra según reglas de negocio.

    Prioridad:
    1️⃣ Compras en el exterior → 5%
    2️⃣ Descuentos por día y monto según el tipo de tarjeta

    Reglas:
    - Classic → No aplica descuento.
    - Gold → 15% Lunes-Miércoles si el monto > 100.
    - Platinum → 20% Lunes-Miércoles (>100), 30% Sábados (>200), 5% exterior.
    - Black → 25% Lunes-Miércoles (>100), 35% Sábados (>200), 5% exterior.
    - White → 25% Lunes-Viernes (>100), 35% Fin de semana (>200), 5% exterior.

    Args:
        card_type (str): Tipo de tarjeta.
        amount (float): Monto de la compra.
        date (datetime): Fecha de la compra.
        purchase_country (str): País donde se realiza la compra.
        client_country (str): País de residencia del cliente.

    Returns:
        tuple[float, str | None]: (tasa de descuento, descripción del beneficio)
    """

    wd = date.weekday()  # 0=Lunes ... 6=Domingo

    # --- CLASSIC ---
    if card_type == CardType.CLASSIC:
        return 0.0, None

    # --- GOLD ---
    if card_type == CardType.GOLD:
        if wd in (0, 1, 2) and amount > 100:
            return 0.15, "Lunes - Miércoles 15%"
        return 0.0, None

    # --- PLATINUM ---
    elif card_type == CardType.PLAT:
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"
        if wd in (0, 1, 2) and amount > 100:
            return 0.20, "Lunes - Miércoles 20%"
        if wd == 5 and amount > 200:
            return 0.30, "Sábado 30%"
        return 0.0, None

    # --- BLACK ---
    elif card_type == CardType.BLACK:
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"
        if wd in (0, 1, 2) and amount > 100:
            return 0.25, "Lunes - Miércoles 25%"
        if wd == 5 and amount > 200:
            return 0.35, "Sábado 35%"
        return 0.0, None

    # --- WHITE ---
    elif card_type == CardType.WHITE:
        # 🚨 Prioridad: exterior antes que día
        if purchase_country != client_country:
            return 0.05, "Exterior 5%"
        if wd in (0, 1, 2, 3, 4) and amount > 100:
            return 0.25, "Lunes - Viernes 25%"
        if wd in (5, 6) and amount > 200:
            return 0.35, "Fin de semana 35%"
        return 0.0, None

    return 0.0, None
