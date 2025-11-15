# Oscar Corredor 14/11/2025 
# *Solución de referencia que implementa dos microservicios en Python (FastAPI) y un frontend en Vue.js,*
# *cumpliendo buenas prácticas de desarrollo, Clean Code y principios SOLID*
# *Microservicios de Productos e Inventario + Frontend Vue*



## Estructura del proyecto

```text
backend/
  product_service/
    app/...
    tests/...
  inventory_service/
    app/...
    tests/...
  requirements.txt
  docker-compose.yml
  product-service.Dockerfile
  inventory-service.Dockerfile
frontend/
  product-inventory-ui/
    src/...
    tests/...
    Dockerfile
docs/
  architecture.md
  diagrams/
    backend-architecture.mmd
    data-flow.mmd
```

## Requisitos previos

- Docker y Docker Compose
- (Opcional) Python 3.11+ y Node 20+ si desea ejecutar sin Docker.

## Ejecución con Docker

1. Ir a la carpeta `backend` y levantar los microservicios:

   ```bash
   cd backend
   docker compose up --build
   ```

   - Product Service: http://localhost:8001/docs
   - Inventory Service: http://localhost:8002/docs

Validar en Docker la crwción de las imagenes
Api Key de las APIS: ENV INTERNAL_API_KEY=super-secret-key


2. En otra terminal, levantar el frontend:

   ```bash
   cd frontend/product-inventory-ui
   docker build -t product-inventory-ui .
   docker run --rm -it -p 5173:5173          -e VITE_API_BASE_URL=http://localhost:8001          -e VITE_INVENTORY_BASE_URL=http://localhost:8002          -e VITE_API_KEY=super-secret-key          product-inventory-ui
   ```

   Frontend disponible en: http://localhost:5173

## Objetivo

1. Crear productos usando Product Service (via Swagger o postman).
2. Inicializar inventario para un producto desde Inventory Service (`POST /api/v1/inventory`).  
3. Desde el frontend, listar productos, ver detalle y realizar compras para actualizar el inventario.

Recuerde enviar siempre el header `X-API-Key: super-secret-key` para consumir los servicios.

## Pruebas backend

Desde cada microservicio:

```bash
cd backend/product_service
pytest --cov=app

cd backend/inventory_service
pytest --cov=app
```

## Pruebas frontend

```bash
cd frontend/product-inventory-ui
npm install
npm test
```

## Propuesta de mejoras para escalabilidad

Validar Diagrama de Arquitectura AWS propuesto

- Separar bases de datos por microservicio (PostgreSQL para productos, Redis/DB para inventarios), se relaciona diagrama en docs\diagrams
- Introducir un API Gateway / BFF que centralice autenticación y versionado.
- Implementar un bus de eventos (Kafka, RabbitMQ) o se puede gestionar con servcios de AWS como SQS  para emitir eventos de cambios de inventario en lugar de logs. y SNS para notifdicar a los usuarios
- Añadir observabilidad (tracing distribuido, métricas y logs estructurados). con servicios como cloudfont y xray
- Desplegar en Kubernetes o ECS de clusters de EC2 con autoescalado HDA y/O KEDA basado en métricas de CPU o RAM.
- Agregar autenticacion con
- OAuth2 / OIDC
- JWT
- API Gateway con validación de tokens
- mTLS entre microservicios (en transito)

## Propuesta de estrategia de Brach (GitFlow) - Feature Branch

Estrategia de ramas (GitFlow)
Se utiliza un modelo GitFlow adaptado:
Master o main: rama estable, lista para producción.
develop: rama de integración continua de features.
Ramas de soporte:
feature/: nuevas funcionalidades ideal cuando hay varios devs trabajando
release/: preparación de releases.
hotfix/: correcciones críticas en producción.

### detalle tecnico solución Backend (microservicios)

1. *Product Service*
   - Framework: **FastAPI**
   - Persistencia: **SQLite (SQL)**
   - Responsabilidades:
     - CRUD completo de productos
     - Paginación con parámetros `page[number]` y `page[size]`
     - Exposición de API bajo `/api/v1/products`
   - Documentación automática con **Swagger/OpenAPI**

2. *Inventory Service*
   - Framework: **FastAPI**
   - Persistencia: **almacenamiento en memoria** (simulando un store simple; como mejora se puede implemntar Redis de elasticache
   - Responsabilidades:
     - Consultar la cantidad disponible de un producto
     - Validar la existencia de productos llamando al Product Service
     - Actualizar inventario tras una compra
     - Emitir eventos básicos vía logs
   - Manejo de resiliencia:
     - Llamadas HTTP al Product Service con **timeouts** y **reintentos (retry)** usando `httpx`
   - Estándar de respuesta: **JSON:API**
   - Documentación automática con **Swagger/OpenAPI**

Ambos microservicios usan:

- Autenticación entre servicios mediante **API Key** (`X-API-Key`)
- Versionado de API vía prefijo: **`/api/v1`**
- Recuerde enviar siempre el header `X-API-Key: super-secret-key` para consumir los servicios.
---

3. *Frontend (SPA)*

- Framework: **Vue.js 3** + **Vite**
- Consumo de API:
  - Product Service (`/api/v1/products`)
  - Inventory Service (`/api/v1/inventory`)
- Funcionalidades:
  - Listar productos con paginación
  - Ver detalles de un producto
  - Ver cantidad disponible en inventario
  - Simular compras y actualizar el inventario
- Manejo de UX:
  - Estados de carga (loading)
  - Manejo de errores de API (control de excepciones)
  - Interfaz sencilla, limpia y funcional

