# 🧱 Imagen base ligera y moderna
FROM python:3.12-slim

# ⚙️ Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

# 📂 Define directorio de trabajo
WORKDIR /app

# 🧩 Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# 🧾 Copia e instala dependencias de Python
COPY requirements.txt .
RUN python -m venv /app/venv && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📦 Copia el resto del código fuente
COPY . .

# 🌐 Expone el puerto 3000 para FastAPI
EXPOSE 3000

# 🚀 Ejecuta el servidor FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
