import os
import httpx # Para hacer llamadas HTTP a otros servicios
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from datetime import datetime 
from fastapi.middleware.cors import CORSMiddleware

ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL", "http://localhost:8000") 
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@host:5432/dbname") 

app = FastAPI(
    title="Document Service",
    description="Servicio para gestionar documentos y orquestar su clasificación ML.",
    version="1.0.0"
)


# --- Configuración CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


ml_client = None

@app.on_event("startup")
async def startup_event():
    global ml_client
    ml_client = httpx.AsyncClient(base_url=ML_SERVICE_URL, timeout=10.0)
    print(f"Document Service iniciando. ML_SERVICE_URL: {ML_SERVICE_URL}")



@app.on_event("shutdown")
async def shutdown_event():
    if ml_client:
        await ml_client.aclose()
        print("Cliente HTTP para ML Service cerrado.")


class DocumentCreate(BaseModel):
   
    title: str = Field(..., example="Informe Financiero Q2")
    content: str = Field(..., example="Este informe detalla los ingresos y gastos del segundo trimestre...")

class DocumentResponse(BaseModel):
    
    id: str = Field(..., example="doc_12345")
    title: str
    content: str
    category: str = Field(None, example="Economía y Finanzas") 
    created_at: str 


# --- 5. Endpoints de la API ---

@app.get("/")
async def read_root():
    
    return {"message": "Document Service is running!"}

@app.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate):

    if not ml_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML Service client not initialized."
        )

    try:
        print(f"Enviando texto al ML Service para clasificación: {doc.title[:50]}...")
        ml_response = await ml_client.post("/classify", json={"text": doc.content})
        ml_response.raise_for_status() 
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