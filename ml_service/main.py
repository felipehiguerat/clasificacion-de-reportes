from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import pandas as pd

app = FastAPI(
    title="Clasificador de Documentos ML Service",
    description="API para clasificar texto de documentos en categorías predefinidas.",
    version="1.0.0"
)


model_path = os.path.join(os.path.dirname(__file__), 'model', 'trained_model.pkl')

# Cargar el modelo al iniciar la aplicación
try:
    model_pipeline = joblib.load(model_path)
    print(f"Modelo cargado exitosamente desde: {model_path}")
except FileNotFoundError:
    print(f"Error: El archivo del modelo no fue encontrado en {model_path}")
    print("Asegúrate de que 'trained_model.pkl' esté en 'ml_service/model/'")
    exit(1) 
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit(1) 


print("Verificando y descargando recursos de NLTK para el servicio...")
try:
    nltk.data.find('corpora/stopwords')
except LookupError: 
    print("Descargando stopwords de NLTK (para el servicio en vivo)...")
    nltk.download('stopwords')
except Exception as e:
    print(f"Error inesperado al verificar/descargar stopwords: {e}")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError: 
    print("Descargando tokenizer 'punkt' de NLTK (para el servicio en vivo)...")
    nltk.download('punkt')
except Exception as e:
    print(f"Error inesperado al verificar/descargar tokenizer 'punkt': {e}")


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


def preprocess_text(text: str) -> str:
   
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text, language='spanish') 
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    return " ".join(tokens)


class DocumentText(BaseModel):
    text: str

-
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

        prediction = model_pipeline.predict([processed_input])[0]
       
        return {"category": prediction} 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al clasificar el documento: {str(e)}")
--
@app.get("/")
async def read_root():
    return {"message": "Servicio de Clasificación de Documentos ML está funcionando."}

