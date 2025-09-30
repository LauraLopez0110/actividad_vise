# Actividad VISE API

Diseñar e implementar una API REST en JSON que procese clientes y compras con diferentes tipos de tarjetas de la empresa ficticia **VISE**.

## 🚀 Requisitos previos
- Python 3.9 o superior
- Git (opcional, si manejas repositorio)

## ⚙️ Instalación y ejecución

1. Clonar el repositorio
   git clone https://github.com/LauraLopez0110/actividad_vise.git
   cd actividad-vise

2. Crear un entorno virtual
   python -m venv venv

3. Activar el entorno virtual
   - En Windows:
     venv\Scripts\activate
   - En Mac/Linux:
     source venv/bin/activate

4. Instalar dependencias
   pip install -r requirements.txt

5. Ejecutar el servidor
   uvicorn app.main:app --reload

6. Probar en el navegador
   - API base: http://127.0.0.1:8000
   - Documentación automática: http://127.0.0.1:8000/docs
   - Documentación alternativa: http://127.0.0.1:8000/redoc

## 📌 Estructura del proyecto

actividad_vise/
│── app/
│ ├── main.py # Punto de entrada FastAPI
│ ├── config.py # Configuración general
│ ├── database.py # Conexión a la base de datos
│ ├── routers/ # Endpoints (clientes, compras, etc.)
│ ├── models/ # Modelos SQLAlchemy
│ ├── schemas/ # Esquemas Pydantic
│ ├── security/ # Seguridad y JWT
│── requirements.txt # Dependencias
│── Dockerfile # Imagen Docker
│── vise_db.db # Base de datos SQLite
│── session.hurl # Tests automáticos
│── README.md # Documentación


## Edpoints principales

| Método | Endpoint         | Descripción               |
| ------ | ---------------- | ------------------------- |
| GET    | `/clientes/`     | Lista todos los clientes  |
| POST   | `/clientes/`     | Crear un nuevo cliente    |
| GET    | `/clientes/{id}` | Obtener un cliente por ID |
| PUT    | `/clientes/{id}` | Actualizar cliente        |
| DELETE | `/clientes/{id}` | Eliminar cliente          |
