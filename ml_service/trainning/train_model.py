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

print("Verificando y descargando recursos de NLTK...")
try:
  
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:

    nltk.data.find('tokenizers/punkt')
except LookupError:
    
    nltk.download('punkt')


try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

print("Recursos de NLTK verificados/descargados.")

def preprocess_text(text):
    # Asegúrate de que el input sea un string, convierte NaN a string vacío
    if pd.isna(text):
        return ""

    text = text.lower() 
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text) 
    tokens = word_tokenize(text, language='spanish') 
    stop_words = set(stopwords.words('spanish')) 
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    return " ".join(tokens)

---
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


print("Preprocesando textos de los documentos...")
df['processed_text'] = df['texto_documento'].apply(preprocess_text)


X = df['processed_text']
y = df['categoria']

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


print("Entrenando el modelo de clasificación...")
pipeline.fit(X_train, y_train)
print("Modelo entrenado exitosamente.")


print("\nEvaluando el rendimiento del modelo en el conjunto de prueba...")
y_pred = pipeline.predict(X_test)

print(classification_report(y_test, y_pred))


model_dir = os.path.join(script_dir, '..', 'model') 
os.makedirs(model_dir, exist_ok=True) 

model_path = os.path.join(model_dir, 'trained_model.pkl')
joblib.dump(pipeline, model_path) 
print(f"\nModelo completo (Pipeline con TfidfVectorizer y SVC) guardado en: {model_path}")

print("\nProceso de entrenamiento completado.")