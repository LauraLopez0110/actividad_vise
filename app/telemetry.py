import os
from azure.monitor.opentelemetry import configure_azure_monitor

def setup_azure_monitor():
    """Inicializa Application Insights si existe la variable de conexión."""
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    if not connection_string:
        print("Application Insights no configurado (falta variable de entorno).")
        return

    try:
        configure_azure_monitor(connection_string=connection_string)
        print("Application Insights configurado correctamente.")
    except Exception as e:
        print(f"Error configurando Application Insights: {e}")
