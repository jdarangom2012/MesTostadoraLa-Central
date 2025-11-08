# AgroInduGestor

Stack: Django 5 + DRF + SimpleJWT, SQL Server, TailwindCSS, logging estructurado y auditoría.

## Instalación backend

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate  # Solo crea tablas de auth; tablas dominio existentes
python manage.py createsuperuser
python manage.py runserver
```

## CSS (Tailwind)
```bash
npm install
npm run build:css  # o npm run watch:css
```

## JWT
Obtener token: POST /api/v1/token/ {"username":"","password":""}

## Auditoría
Todas las operaciones CRUD generan filas en dbo.tblLogEventos mediante señales.

## Correlation ID
Enviar cabecera `X-Correlation-Id` para trazar; sino se genera UUID.

## Paginación y filtros
La API usa paginación por página (PageNumberPagination) con tamaño 25 por defecto (configurable vía `API_PAGE_SIZE`).
Busca automáticamente sobre campos de texto si el viewset no define `search_fields` usando query param `?search=...`.
Ordenamiento dinámico con `?ordering=campo` o `?ordering=-campo`.

## Producción (ejemplo)
```bash
gunicorn mes_central.wsgi:application --bind 0.0.0.0:8000
# ASGI (si se requiere websockets / performance IO):
uvicorn mes_central.asgi:application --host 0.0.0.0 --port 8000
```

Detallar configuración Nginx y systemd fuera de este alcance.
