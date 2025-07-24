# Usa la misma imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala Poetry
RUN pip install poetry==1.8.2

# Copia los archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instala las dependencias del proyecto usando Poetry
# --no-root: no instala el proyecto como un paquete
# --no-dev: no instala dependencias de desarrollo
# --sync: sincroniza el entorno con el lock file, eliminando lo que no esté
RUN poetry install --no-root --no-dev --sync

# Copia el código de tu aplicación

COPY main.py ./

# Expone el puerto en el que correrá tu API de FastAPI (8000 es el puerto por defecto de Uvicorn)
EXPOSE 8000

# Comando para correr la aplicación cuando el contenedor se inicie
# Asegúrate de que main:app apunta al objeto 'app' en tu main.py
# Asegúrate de que las variables de entorno necesarias (ML_SERVICE_URL, DATABASE_URL)
# se pasen cuando ejecutes el contenedor Docker (con -e o un archivo .env si usas docker-compose)
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]