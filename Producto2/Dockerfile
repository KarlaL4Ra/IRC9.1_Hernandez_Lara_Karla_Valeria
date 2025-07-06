# Imagen base oficial de Python
FROM python:3.10-slim

# Instala dependencias necesarias para Ansible y WeasyPrint
RUN apt-get update && \
    apt-get install -y \
        ansible \
        sudo \
        build-essential \
        libpango1.0-0 \
        libcairo2 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        zlib1g-dev \
        libpq-dev && \
    apt-get clean

# Crea directorio de trabajo
WORKDIR /app

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Exponer el puerto del servidor Flask
EXPOSE 5000

# Ejecutar la app Flask
CMD ["python", "app/main.py"]
