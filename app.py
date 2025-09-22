from fastapi import FastAPI

app = FastAPI(title="Actividad VISE API")

# Endpoint base de prueba
@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Actividad VISE 🚀"}

# Endpoint para registrar clientes
@app.post("/client")
def register_client(client: dict):
    # 👇 Aquí luego se implementarán validaciones de restricciones
    return {"status": "Pending", "message": "Lógica de registro por implementar"}

# Endpoint para procesar compras
@app.post("/purchase")
def process_purchase(purchase: dict):
    # 👇 Aquí luego se aplicarán restricciones y beneficios
    return {"status": "Pending", "message": "Lógica de compra por implementar"}
