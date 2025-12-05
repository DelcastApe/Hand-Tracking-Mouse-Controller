FROM python:3.11-slim

# Instalar dependencias del sistema para OpenCV y GUI
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY src ./src

# Comando por defecto
CMD ["python", "src/main.py"]
