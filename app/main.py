# ==============================
# 📡 VISE API - Observabilidad con Grafana Cloud + Azure Application Insights
# ==============================

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client, purchases

# Cargar variables de entorno
load_dotenv()

# --- Configurar OpenTelemetry para Grafana Cloud ---
from opentelemetry import trace, metrics, _logs
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

# Instrumentadores
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Integración con Azure Application Insights
from app.telemetry import setup_azure_monitor


def setup_otel(service_name: str = "vise-api"):
    """Configura exportadores OTLP para Grafana Cloud y Azure Insights."""
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").rstrip("/")
    headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")

    resource = Resource.create({
        "service.name": service_name,
        "service.namespace": "vise",
        "deployment.environment": "production",
    })

    # --- Traces ---
    tracer_provider = TracerProvider(resource=resource)
    if endpoint and headers:
        tracer_provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=f"{endpoint}/v1/traces",
                    headers={"Authorization": headers},
                )
            )
        )
    trace.set_tracer_provider(tracer_provider)

    # --- Metrics ---
    if endpoint and headers:
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(
                endpoint=f"{endpoint}/v1/metrics",
                headers={"Authorization": headers},
            )
        )
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)

    # --- Logs ---
    logger_provider = LoggerProvider(resource=resource)
    if endpoint and headers:
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(
                OTLPLogExporter(
                    endpoint=f"{endpoint}/v1/logs",
                    headers={"Authorization": headers},
                )
            )
        )
    _logs.set_logger_provider(logger_provider)

    LoggingInstrumentor().instrument(set_logging_format=True)
    RequestsInstrumentor().instrument()

    print("✅ OpenTelemetry configurado para Grafana Cloud.")


# --- Inicializar ambos sistemas de observabilidad ---
setup_otel()
setup_azure_monitor()

# --- Inicializar aplicación FastAPI ---
app = FastAPI(title="VISE API - Clientes y Compras")

Base.metadata.create_all(bind=engine)
FastAPIInstrumentor().instrument_app(app)
StarletteInstrumentor().instrument_app(app)

# Registrar routers
app.include_router(client.router)
app.include_router(purchases.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API (Grafana + Azure Monitor) 🚀"}
