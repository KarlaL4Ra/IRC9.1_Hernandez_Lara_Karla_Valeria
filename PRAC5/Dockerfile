# Usar imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente a /app
COPY src/ .

# Exponer el puerto por defecto de la app
EXPOSE 5000

# Variables de entorno por defecto
ENV APP_VERSION=1.0.0

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
