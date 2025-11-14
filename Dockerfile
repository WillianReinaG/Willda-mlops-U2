# Dockerfile para aplicación de diagnóstico médico
# Imagen basada en Python ligera que expone el servicio en el puerto 5000

# Usar imagen oficial de Python 3.11 slim (ligera)
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py Diagnostico.py test_diagnostico.py ./
COPY templates/ ./templates/

# Crear directorio para datos persistentes
RUN mkdir -p /app/data

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Exponer puerto 5000
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Volumen para datos persistentes
VOLUME ["/app/data"]

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]


