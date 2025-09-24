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
   uvicorn app:app --reload

6. Probar en el navegador
   - API base: http://127.0.0.1:8000
   - Documentación automática: http://127.0.0.1:8000/docs


## 📌 Estructura del proyecto
actividad-vise/
│
├── app.py             # Código principal de la API
├── requirements.txt   # Dependencias
├── README.md          # Documentación
└── venv/              # Entorno virtual (ignorado en Git)


## Instrucciones para correr el docker

docker build -t vise-api .
docker run -p 8000:8000 vise-api