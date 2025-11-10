from fastapi import FastAPI
from app.database import Base, engine
from app.routers import client, purchases

# 🧩 Importar OpenTelemetry
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
import exporter  # 👈 tu archivo exporter.py configurado con Axiom

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Crear la app
app = FastAPI(title="VISE API - Clientes y Compras")

# 🧠 Instrumentar automáticamente FastAPI con OpenTelemetry
FastAPIInstrumentor.instrument_app(app)
app.add_middleware(OpenTelemetryMiddleware)

# Registrar routers
app.include_router(client.router)
app.include_router(purchases.router)

@app.get("/")
def read_root():
    with exporter.tracer.start_as_current_span("root_request_span"):
        return {"message": "Welcome to the VISE API"}
