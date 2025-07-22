# Usa una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# --- SECCIÓN DE INSTALACIÓN DE POETRY MEJORADA ---
# Establece el directorio de instalación de Poetry
ENV POETRY_HOME="/usr/local/poetry"
# Agrega el directorio bin de Poetry a la PATH del sistema
# /usr/local/bin ya suele estar en la PATH por defecto en muchas imágenes Linux,
# pero lo hacemos explícito para mayor robustez.
ENV PATH="$POETRY_HOME/bin:$PATH"

# Descarga e instala Poetry usando pip (más directo y fiable en Docker)
# poetry se instalará en /usr/local/poetry/bin
RUN pip install poetry==1.8.2

# Configura Poetry para que cree entornos virtuales dentro del directorio del proyecto
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# --- FIN DE SECCIÓN DE INSTALACIÓN DE POETRY MEJORADA ---


# Copia los archivos de configuración de Poetry para instalar las dependencias
COPY pyproject.toml poetry.lock ./

# Instala las dependencias del proyecto (incluyendo Flask, scikit-learn, NLTK, pandas)
# --no-root: No instala tu propio paquete 'ml_service' (si no es necesario)
# --no-dev: No instala las dependencias de desarrollo
# --sync: Sincroniza el entorno con poetry.lock, eliminando paquetes que no estén en él.
RUN poetry install --no-root --no-dev --sync

# Descarga los recursos de NLTK durante la construcción de la imagen
# Esto asegura que los modelos de NLTK estén disponibles dentro del contenedor
RUN poetry run python -c "import nltk; \
               nltk.download('stopwords'); \
               nltk.download('punkt'); \
               nltk.download('averaged_perceptron_tagger'); \
               nltk.download('punkt_tab');"

# Copia el código de tu servicio y el modelo entrenado
# Asegúrate de que las rutas relativas sean correctas
COPY main.py ./
COPY model/trained_model.pkl ./model/

# Expone el puerto en el que correrá la aplicación Flask (Gunicorn)
EXPOSE  8000

# Comando para ejecutar la aplicación usando Gunicorn (servidor WSGI)
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]