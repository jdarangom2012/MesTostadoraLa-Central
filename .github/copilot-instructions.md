# Guía para Agentes AI: MesTostadoraLa-Central

## Arquitectura y Componentes
- **Backend:** Django 5 + DRF + SimpleJWT. Modular por dominio: cada carpeta (`clientes`, `empaques`, etc.) contiene `models.py`, `serializers.py`, `views.py`, `viewsets.py`, `urls.py`, `admin.py`.
- **Base de datos:** SQL Server (tablas de dominio ya existen; migraciones solo para auth y core).
- **Frontend:** HTML en `templates/`, CSS con TailwindCSS compilado vía npm (`css/styles.css`, `css/mes.css`).
- **Auditoría:** Señales Django generan logs automáticos en `dbo.tblLogEventos`.
- **Configuración global:** Carpeta `core/` (middleware, logging, roles, filtros, señales).

## Flujos de Desarrollo
- Instala dependencias Python: `pip install -r requirements.txt`.
- Migraciones: `python manage.py migrate` (solo auth/core).
- Superusuario: `python manage.py createsuperuser`.
- Servidor dev: `python manage.py runserver` o tarea VSCode "Run Django dev server (no reload)".
- Producción: `gunicorn mes_central.wsgi:application --bind 0.0.0.0:8000` o `uvicorn mes_central.asgi:application --host 0.0.0.0 --port 8000`.
- CSS: `npm install` y luego `npm run build:css` o `npm run watch:css`.

## Patrones y Convenciones
- **Autenticación:** JWT vía SimpleJWT (`/api/v1/token/`).
- **Auditoría:** CRUD logueado automáticamente por señales.
- **Correlation ID:** Middleware usa `X-Correlation-Id` (se genera UUID si no existe).
- **Paginación:** `PageNumberPagination`, tamaño por defecto 25.
- **Búsqueda y orden:** `?search=...` y `?ordering=campo` en endpoints DRF.
- **Frontend:** Usa `{% static %}` para recursos, paleta centralizada en Tailwind (`head.html`).

## Integraciones y Dependencias
- **DRF:** Viewsets para CRUD, filtros y paginación automáticos.
- **TailwindCSS:** Configuración en `head.html`, compilación vía npm.
- **SQL Server:** Conexión y tablas de dominio preexistentes.

## Ejemplos y Archivos Clave
- Ejemplo de viewset: `clientes/viewsets.py`, `empaques/viewsets.py`.
- Ejemplo de señal de auditoría: `core/signals.py`.
- Ejemplo de middleware: `core/middleware.py` (Correlation ID).
- Configuración de estilos: `templates/includes/head.html`.
- Comandos principales: ver `README.md`.

---

**Actualiza esta guía si cambian flujos, dependencias o convenciones. Solicita feedback si alguna sección no es clara o falta información relevante.**
