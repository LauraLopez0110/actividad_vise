# ==============================
# 📡 VISE API - Observabilidad con Grafana Cloud + OpenTelemetry
# ==============================

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client, purchases

# --- 1️⃣ Cargar variables de entorno ---
load_dotenv()  # Debe ejecutarse antes de configurar OpenTelemetry


# --- 2️⃣ Configurar OpenTelemetry ---
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


def setup_otel(service_name: str = "vise-api"):
    """Configura exportadores OTLP para traces, métricas y logs hacia Grafana Cloud."""
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").rstrip("/")
    headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")
    protocol = os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")

    if not endpoint or not headers:
        print("⚠️  [OpenTelemetry] Variables de entorno incompletas. No se exportarán métricas a Grafana Cloud.")
        return

    resource = Resource.create({
        "service.name": service_name,
        "service.namespace": "vise",
        "deployment.environment": "production",
    })

    # --- Traces ---
    tracer_provider = TracerProvider(resource=resource)
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
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(
            OTLPLogExporter(
                endpoint=f"{endpoint}/v1/logs",
                headers={"Authorization": headers},
            )
        )
    )
    _logs.set_logger_provider(logger_provider)

    # --- Instrumentaciones comunes ---
    LoggingInstrumentor().instrument(set_logging_format=True)
    RequestsInstrumentor().instrument()

    print("✅ OpenTelemetry configurado correctamente para Grafana Cloud.")


# --- 3️⃣ Inicializar OpenTelemetry ---
setup_otel()


# --- 4️⃣ Inicializar aplicación FastAPI ---
app = FastAPI(title="VISE API - Clientes y Compras")

# Crear las tablas del ORM
Base.metadata.create_all(bind=engine)

# Instrumentar la app FastAPI + Starlette para trazas automáticas
FastAPIInstrumentor().instrument_app(app)
StarletteInstrumentor().instrument_app(app)

# Registrar los routers
app.include_router(client.router)
app.include_router(purchases.router)


# --- 5️⃣ Endpoint raíz ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API"}

