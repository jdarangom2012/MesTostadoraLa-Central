# Copilot Instructions for AgroInduGestor

## Arquitectura General
- Proyecto Django 5 + Django REST Framework (DRF) + SimpleJWT, con SQL Server como base de datos.
- Estructura modular: cada dominio (ej. `clientes`, `empaques`, `curvas_tueste`, etc.) tiene su propio directorio con modelos, serializers, views, viewsets y urls.
- Auditoría y logging estructurado: todas las operaciones CRUD generan eventos en `dbo.tblLogEventos` mediante señales.
- Frontend usa TailwindCSS, compilado vía npm scripts.

## Flujos de Desarrollo
- **Backend:**
  - Instalar dependencias con `pip install -r requirements.txt`.
  - Migraciones: `python manage.py migrate` (solo crea tablas de auth; tablas de dominio ya existen en la BD).
  - Crear superusuario: `python manage.py createsuperuser`.
  - Servidor de desarrollo: `python manage.py runserver`.
  - Producción: `gunicorn mes_central.wsgi:application --bind 0.0.0.0:8000` o `uvicorn mes_central.asgi:application --host 0.0.0.0 --port 8000`.
- **Frontend (CSS):**
  - Instalar dependencias con `npm install`.
  - Compilar CSS: `npm run build:css` o `npm run watch:css`.

## Convenciones y Patrones
- **Autenticación:** JWT vía SimpleJWT. Obtener token con POST `/api/v1/token/`.
- **Auditoría:** Todas las operaciones CRUD generan logs automáticos.
- **Correlation ID:** Usar cabecera `X-Correlation-Id` para trazabilidad; si no se envía, se genera un UUID.
- **Paginación y Filtros:**
  - Paginación por página (`PageNumberPagination`), tamaño por defecto 25 (configurable).
  - Búsqueda automática en campos de texto si el viewset no define `search_fields` (`?search=...`).
  - Ordenamiento dinámico con `?ordering=campo` o `?ordering=-campo`.
- **Estructura de carpetas:**
  - Cada app tiene: `models.py`, `serializers.py`, `views.py`, `viewsets.py`, `urls.py`, `admin.py`.
  - Plantillas HTML en `templates/`.
  - Configuración global en `core/`.

## Integraciones y Dependencias
- **Base de datos:** SQL Server (tablas de dominio preexistentes).
- **CSS:** TailwindCSS vía npm.
- **API:** DRF, JWT, paginación, filtros y ordenamiento.

## Ejemplos de Patrones
- Viewsets DRF para CRUD y filtros automáticos.
- Señales Django para logging/auditoría.
- Uso de `X-Correlation-Id` en middleware para trazabilidad.

## Archivos Clave
- `manage.py`: comandos Django.
- `requirements.txt`: dependencias Python.
- `core/`: configuración, middleware, logging, roles.
- `templates/`: HTML base y componentes.
- `README.md`: guía de instalación y comandos principales.

---

**Actualiza esta guía si cambian flujos, dependencias o convenciones. Solicita feedback si alguna sección no es clara o falta información relevante.**
