import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# --- 1. Descargar recursos de NLTK (solo la primera vez) ---
# Es posible que necesites ejecutar esto la primera vez para descargar los datos de lenguaje.
# Poetry instala NLTK, pero los datos específicos de idiomas se descargan aparte.
print("Verificando y descargando recursos de NLTK...")
try:
    # Intenta cargar stopwords, si no, las descarga
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    # Intenta cargar punkt, si no, lo descarga
    nltk.data.find('tokenizers/punkt')
except LookupError:
    # Descargando 'punkt' que incluye modelos para tokenización de frases
    nltk.download('punkt')

# También descargar el pack de 'averaged_perceptron_tagger' que a veces es una dependencia implícita
# de otras operaciones de NLTK, aunque no lo usemos directamente aquí.
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

print("Recursos de NLTK verificados/descargados.")

# --- 2. Función de Preprocesamiento de Texto ---
def preprocess_text(text):
    # Asegúrate de que el input sea un string, convierte NaN a string vacío
    if pd.isna(text): # <--- RE-INCLUIR ESTO para robustez con datos nulos
        return ""

    text = text.lower() # Convertir a minúsculas
    text = re.sub(r'\d+', '', text) # Eliminar números
    text = re.sub(r'[^\w\s]', '', text) # Eliminar puntuación (mantener solo letras y espacios)
    tokens = word_tokenize(text, language='spanish') # <--- ¡CLAVE: CORREGIDO AQUÍ!
    stop_words = set(stopwords.words('spanish')) # Stopwords en español (palabras comunes sin significado como "el", "la")
    # Eliminar stopwords y palabras de un solo caracter
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    return " ".join(tokens)

# --- 3. Cargar Datos ---
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, 'data', 'reportes.csv')

try:
    df = pd.read_csv(data_path)
    print(f"\nDataset cargado desde: {data_path}")
    print(f"Total de documentos: {len(df)}")
    print("Categorías únicas encontradas:", df['categoria'].unique())
except FileNotFoundError:
    print(f"Error: El archivo {data_path} no fue encontrado.")
    print("Asegúrate de que 'documentos_soporte.csv' esté en 'ml_service/training/data/'")
    exit()

# --- 4. Preprocesar los Textos ---
print("Preprocesando textos de los documentos...")
df['processed_text'] = df['texto_documento'].apply(preprocess_text)

# --- 5. Dividir los Datos en Conjuntos de Entrenamiento y Prueba ---
# X son las características (texto), y es la etiqueta (categoría)
X = df['processed_text']
y = df['categoria']
# Dividimos el 80% para entrenamiento y 20% para prueba
# 'stratify=y' asegura que la proporción de categorías sea similar en ambos conjuntos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Tamaño del conjunto de entrenamiento: {len(X_train)}")
print(f"Tamaño del conjunto de prueba: {len(X_test)}")

# --- 6. Crear el Pipeline del Modelo ---
# Un Pipeline encadena varios pasos de procesamiento de datos y modelado.
# Aquí: 1. Vectorización TF-IDF (convierte texto en números). 2. Clasificador SVM.
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()), # Transforma el texto en una matriz TF-IDF
    ('classifier', SVC(kernel='linear', probability=True)) # Support Vector Classifier, 'linear' funciona bien para texto
])

# --- 7. Entrenar el Modelo ---
print("Entrenando el modelo de clasificación...")
pipeline.fit(X_train, y_train)
print("Modelo entrenado exitosamente.")

# --- 8. Evaluar el Modelo ---
print("\nEvaluando el rendimiento del modelo en el conjunto de prueba...")
y_pred = pipeline.predict(X_test)
# Muestra un informe detallado de precisión, recall, f1-score por categoría
print(classification_report(y_test, y_pred))

# --- 9. Guardar el Modelo Entrenado ---
# Guardamos el pipeline completo (vectorizador + clasificador) para usarlo después
model_dir = os.path.join(script_dir, '..', 'model') # Ruta a clasificador-documentos/ml_service/model
os.makedirs(model_dir, exist_ok=True) # Crea la carpeta 'model' si no existe

model_path = os.path.join(model_dir, 'trained_model.pkl')
joblib.dump(pipeline, model_path) # Usa joblib para guardar el pipeline
print(f"\nModelo completo (Pipeline con TfidfVectorizer y SVC) guardado en: {model_path}")

print("\nProceso de entrenamiento completado.")