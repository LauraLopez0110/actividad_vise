# --- OpenTelemetry setup (console exporters) ---
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

# Logs (en 1.38.x usan los módulos con guion bajo)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry import _logs

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def setup_otel(service_name: str = "vise-api"):
    # Recurso común (nombre del servicio)
    resource = Resource.create({"service.name": service_name})

    # ---- Traces ----
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    # ---- Metrics ----
    metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # ---- Logs ----
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogExporter()))
    _logs.set_logger_provider(logger_provider)

    # ---- Instrumentación de librerías ----
    # Captura de logs de logging estándar (con trace_id/span_id)
    LoggingInstrumentor().instrument(set_logging_format=True)
    # HTTP sync
    RequestsInstrumentor().instrument()

# Llama la configuración ANTES de crear la app FastAPI
setup_otel()
# --- Fin OpenTelemetry setup ---


from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client, purchases

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VISE API - Clientes y Compras")

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.starlette import StarletteInstrumentor

FastAPIInstrumentor().instrument_app(app)
StarletteInstrumentor().instrument_app(app)

# Registrar routers
app.include_router(client.router)
app.include_router(purchases.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the VISE API"}
