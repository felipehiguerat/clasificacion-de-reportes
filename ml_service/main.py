from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import pandas as pd # Importar pandas para pd.isna

# --- 1. Inicialización de FastAPI ---
app = FastAPI(
    title="Clasificador de Documentos ML Service",
    description="API para clasificar texto de documentos en categorías predefinidas.",
    version="1.0.0"
)

# --- 2. Cargar el Modelo Entrenado ---
# La ruta al modelo debe ser relativa a donde se ejecuta el script main.py
# Si main.py está en ml_service/, entonces el modelo está en ml_service/model/
model_path = os.path.join(os.path.dirname(__file__), 'model', 'trained_model.pkl')

# Cargar el modelo al iniciar la aplicación
try:
    model_pipeline = joblib.load(model_path)
    print(f"Modelo cargado exitosamente desde: {model_path}")
except FileNotFoundError:
    print(f"Error: El archivo del modelo no fue encontrado en {model_path}")
    print("Asegúrate de que 'trained_model.pkl' esté en 'ml_service/model/'")
    exit(1) # Usar exit(1) para indicar un error
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit(1) # Usar exit(1) para indicar un error

# --- 3. Descargar recursos de NLTK (se ejecutará al inicio de la aplicación o en el build de Docker) ---
# Esto es importante para el preprocesamiento de texto en tiempo de ejecución
print("Verificando y descargando recursos de NLTK para el servicio...")
try:
    nltk.data.find('corpora/stopwords')
except LookupError: # Corregido: Usar LookupError
    print("Descargando stopwords de NLTK (para el servicio en vivo)...")
    nltk.download('stopwords')
except Exception as e:
    print(f"Error inesperado al verificar/descargar stopwords: {e}")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError: # Corregido: Usar LookupError
    print("Descargando tokenizer 'punkt' de NLTK (para el servicio en vivo)...")
    nltk.download('punkt')
except Exception as e:
    print(f"Error inesperado al verificar/descargar tokenizer 'punkt': {e}")

# Descargar también averaged_perceptron_tagger y punkt_tab explícitamente si es necesario
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
except Exception as e:
    print(f"Error inesperado al verificar/descargar averaged_perceptron_tagger: {e}")

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
except Exception as e:
    print(f"Error inesperado al verificar/descargar punkt_tab: {e}")

print("Recursos de NLTK verificados/descargados para el servicio.")

# --- 4. Función de Preprocesamiento de Texto (igual que en train_model.py) ---
def preprocess_text(text: str) -> str:
    # Manejar valores nulos/NaN
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text, language='spanish') # Corregido: especificar idioma
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    return " ".join(tokens)

# --- 5. Definición del Modelo de Datos para la Solicitud (Pydantic) ---
class DocumentText(BaseModel):
    text: str

# --- 6. Definición de la Ruta (Endpoint) de la API ---
@app.post("/classify")
async def classify_document(document: DocumentText):
    """
    Clasifica el texto de un documento en una categoría predefinida.
    """
    if not document.text:
        raise HTTPException(status_code=400, detail="El texto del documento no puede estar vacío.")

    try:
        # Preprocesar el texto de entrada
        processed_input = preprocess_text(document.text)

        # Realizar la predicción
        # El pipeline ya contiene el vectorizador y el clasificador
        prediction = model_pipeline.predict([processed_input])[0]
        # Si el modelo soporta probabilidades, puedes obtenerlas así:
        # probabilities = model_pipeline.predict_proba([processed_input])[0]
        # category_probabilities = {model_pipeline.classes_[i]: prob for i, prob in enumerate(probabilities)}

        return {"category": prediction} # , "probabilities": category_probabilities}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al clasificar el documento: {str(e)}")

# --- 7. Ruta de Bienvenida (Opcional) ---
@app.get("/")
async def read_root():
    return {"message": "Servicio de Clasificación de Documentos ML está funcionando."}

# --- 8. Cómo Ejecutar la Aplicación (para desarrollo) ---
# Para ejecutar esta aplicación, usarías Uvicorn desde la terminal:
# poetry run uvicorn main:app --host 0.0.0.0 --port 8000
# main:app significa el objeto 'app' dentro del archivo 'main.py'