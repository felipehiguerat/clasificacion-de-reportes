import os
import httpx # Para hacer llamadas HTTP a otros servicios
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from datetime import datetime 
# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# --- 1. Configuración del Servicio ---
# Usamos variables de entorno para la configuración.
# Es crucial que estas variables estén configuradas cuando ejecutes el servicio.
ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL", "http://localhost:8000") # URL de tu ml_service
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@host:5432/dbname") # URL de tu DB PostgreSQL

# --- 2. Inicialización de FastAPI ---
app = FastAPI(
    title="Document Service",
    description="Servicio para gestionar documentos y orquestar su clasificación ML.",
    version="1.0.0"
)

# --- 3. Cliente HTTP para el ML Service ---
# Usamos httpx.AsyncClient para llamadas asíncronas y eficientes.
# Se inicializa y cierra en los eventos de startup/shutdown de FastAPI.
ml_client = None

@app.on_event("startup")
async def startup_event():
    global ml_client
    ml_client = httpx.AsyncClient(base_url=ML_SERVICE_URL, timeout=10.0)
    print(f"Document Service iniciando. ML_SERVICE_URL: {ML_SERVICE_URL}")

    # --- Configuración de la Base de Datos (SQLAlchemy - Comentado por ahora) ---
    # Esto es un placeholder. La configuración real de la DB y los modelos
    # requerirían más detalles (como definir modelos ORM, tablas, etc.)
    # engine = create_engine(DATABASE_URL)
    # Base.metadata.create_all(bind=engine) # Crea las tablas si no existen
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # print(f"Conexión a la base de datos intentada: {DATABASE_URL.split('@')[-1]}")


@app.on_event("shutdown")
async def shutdown_event():
    if ml_client:
        await ml_client.aclose()
        print("Cliente HTTP para ML Service cerrado.")

# --- 4. Modelos de Datos (Pydantic) ---

class DocumentCreate(BaseModel):
    """Modelo para crear un nuevo documento."""
    title: str = Field(..., example="Informe Financiero Q2")
    content: str = Field(..., example="Este informe detalla los ingresos y gastos del segundo trimestre...")

class DocumentResponse(BaseModel):
    """Modelo para la respuesta de un documento."""
    id: str = Field(..., example="doc_12345")
    title: str
    content: str
    category: str = Field(None, example="Economía y Finanzas") # La categoría puede ser None inicialmente
    created_at: str # Usamos string para simplificar la fecha/hora aquí


# --- 5. Endpoints de la API ---

@app.get("/")
async def read_root():
    """Endpoint de bienvenida y salud del servicio."""
    return {"message": "Document Service is running!"}

@app.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate):
    """
    Recibe un nuevo documento, lo clasifica usando el ML Service
    y (conceptualmente) lo almacena en la base de datos.
    """
    if not ml_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML Service client not initialized."
        )

    # Paso 1: Clasificar el documento usando el ml_service
    try:
        print(f"Enviando texto al ML Service para clasificación: {doc.title[:50]}...")
        ml_response = await ml_client.post("/classify", json={"text": doc.content})
        ml_response.raise_for_status() # Lanza una excepción para errores HTTP (4xx o 5xx)
        classification_result = ml_response.json()
        category = classification_result.get("category", "Uncategorized")
        print(f"Documento '{doc.title}' clasificado como: {category}")

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al conectar con ML Service: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error del ML Service: {exc.response.text}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al clasificar: {exc}"
        )

    # Paso 2: Simular almacenamiento en base de datos (aquí iría tu lógica de DB real)
    # Por ahora, solo creamos un ID ficticio y una marca de tiempo.
    document_id = f"doc_{os.urandom(4).hex()}"
    # db_document = DocumentDB(
    #     id=document_id,
    #     title=doc.title,
    #     content=doc.content,
    #     category=category,
    #     created_at=datetime.utcnow()
    # )
    # db.add(db_document)
    # db.commit()
    # db.refresh(db_document)

    # Devolver la respuesta
    return DocumentResponse(
        id=document_id,
        title=doc.title,
        content=doc.content,
        category=category,
        created_at=str(datetime.utcnow()) # Convertir a string para la respuesta
    )

# --- 6. Modelo de Base de Datos (SQLAlchemy - Comentado por ahora) ---
# Base = declarative_base()

# class DocumentDB(Base):
#     __tablename__ = "documents"
#     id = Column(String, primary_key=True, index=True)
#     title = Column(String, index=True)
#     content = Column(String)
#     category = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)