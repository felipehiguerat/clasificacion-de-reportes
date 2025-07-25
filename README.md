# 🚀 Sistema de Clasificación de Documentos con Microservicios

Este proyecto implementa una arquitectura de microservicios para la **clasificación automática de documentos**, separando la lógica de gestión de documentos de la inteligencia de Machine Learning (ML).

---

## 🌟 Visión General

El sistema consta de **dos microservicios principales**:

- **`document_service`**: 
  - Gestiona la recepción y almacenamiento (simulado).
  - Orquesta la clasificación de documentos.
  - Punto de entrada principal para clientes o frontend.

- **`ml_service`**: 
  - Servicio especializado en la **clasificación de texto**.
  - Utiliza un modelo de Machine Learning.
  - Expone su funcionalidad a través de una API REST.

La comunicación entre servicios se realiza mediante **peticiones HTTP**, y ambos están encapsulados en contenedores Docker.

---

## 🛠️ Tecnologías Clave

- **Backend y Servicios**: FastAPI, Python
- **Frontend (Opcional / Ilustrativo)**: Cualquier cliente que consuma APIs REST
- **Contenerización y Orquestación**: Docker

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph LR
    A[Frontend/Cliente] -- HTTP POST /documents --> B(Document Service:8001)
    B -- HTTP POST /classify (contenido) --> C(ML Service:8000)
    C -- Clasificación (categoría) --> B
    B -- Documento Clasificado (JSON) --> A
```

---
El document_service actúa como orquestador.

El ml_service se especializa en la clasificación de texto.

Toda la comunicación se realiza mediante REST APIs.

Docker garantiza un entorno homogéneo y fácil despliegue.
--

## 🌟 importacia para empresas

✅ Resiliencia y Menor Downtime
Si el ml_service falla, el document_service sigue operando, asegurando alta disponibilidad.

✅ Escalabilidad y Optimización de Costos
Cada servicio puede escalarse de forma independiente según la demanda.

✅ Agilidad en Desarrollo y Despliegue
Permite actualizaciones individuales sin afectar el sistema completo.

✅ Flexibilidad Tecnológica
Cada servicio puede usar el lenguaje y stack más adecuado para su rol.

✅ Mantenibilidad
Bases de código pequeñas, más fáciles de depurar y evolucionar.
--
