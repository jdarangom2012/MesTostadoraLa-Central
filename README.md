🏭 AgroInduGestor — MES para Plantas Agroindustriales

Mostrar imagen
Mostrar imagen
Mostrar imagen
Mostrar imagen
Mostrar imagen
Mostrar imagen

AgroInduGestor es un Sistema de Ejecución de Manufactura (MES) para la industria agroindustrial desarrollado por NautilusTech S.A.S. — integra producción, calidad, trazabilidad y reportes en tiempo real conectando sistemas OT (SCADA/PLC) con sistemas IT (SAP/ERP).


🎯 Problema que resuelve

Las plantas agroindustriales — cafeteras, de alimentos, de procesamiento — gestionan su producción con registros en papel, Excel o sistemas desconectados de su ERP. AgroInduGestor conecta el piso de planta con el sistema de gestión, capturando datos en tiempo real de SCADA y PLC, y entregando KPIs de producción a gerencia sin intervención manual.


✨ Módulos del sistema

MóduloDescripción⚙️ ProducciónRegistro y seguimiento de órdenes de producción en tiempo real📦 InventarioControl de materias primas, insumos y producto terminado✅ CalidadRegistro de controles de calidad, muestreos y no conformidades🔍 TrazabilidadTrazabilidad completa lote a lote desde materia prima hasta despacho☕ MoliendaMódulo especializado para proceso de molienda (industria cafetera)📦 EmpaqueControl de líneas de empaque con conteo automatizado📊 Reportes Power BIDashboards ejecutivos conectados a datos de planta en tiempo real🔗 Integración SAPSincronización bidireccional con SAP mediante REST API🖥️ Dashboard TVPantallas industriales con KPIs en tiempo real para operadores📋 AuditoríaLog completo de todas las operaciones con Correlation ID


🛠️ Stack tecnológico

Backend:       Python 3.12 + Django 5.0 + Django REST Framework
Base datos:    SQL Server 2019 (integración con BD existente de planta)
Auth:          JWT (SimpleJWT)
Integración:   SAP RFC + SCADA OPC-UA + PLC Mitsubishi/Siemens
BI:            Power BI conectado via API REST
Despliegue:    Azure VM + Docker + Gunicorn
Auditoría:     Logging estructurado + Correlation ID


🏗️ Arquitectura OT/IT

PLANTA (OT Layer)
┌─────────────────────────────────────┐
│  PLC Mitsubishi │  PLC Siemens      │
│  Sensores IoT   │  Básculas         │
└──────────┬──────────────────────────┘
           │ SCADA / OPC-UA
┌──────────▼──────────────────────────┐
│         SCADA Server                │
│   (Captura datos en tiempo real)    │
└──────────┬──────────────────────────┘
           │ REST API / DB directa
SISTEMA IT (AgroInduGestor)
┌──────────▼──────────────────────────┐
│         DJANGO BACKEND              │
│  ┌─────────┐  ┌─────────────────┐  │
│  │  API    │  │  ETL Pipelines  │  │
│  │  REST   │  │  SCADA → DB     │  │
│  └─────────┘  └─────────────────┘  │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│  SQL Server  │  SAP ERP  │ Power BI │
└─────────────────────────────────────┘


🔧 Características técnicas destacadas

Integración SCADA/PLC

python# Captura de datos OT en tiempo real
# Conexión con PLCs Mitsubishi y Siemens
# Procesamiento de señales analógicas y digitales
# Almacenamiento en SQL Server con timestamp de planta

API REST con auditoría completa

python# Todas las operaciones CRUD generan registro en tblLogEventos
# Correlation ID para trazabilidad de requests
# JWT con refresh tokens y control de sesión

# Ejemplo endpoint
GET /api/v1/produccion/ordenes/?search=lote-2024&ordering=-fecha_inicio
POST /api/v1/calidad/muestreos/
GET /api/v1/reportes/kpi-diario/?planta=central&turno=1

Paginación y filtros dinámicos

python# PageNumberPagination con tamaño configurable (default: 25)
# ?search= busca automáticamente en campos de texto
# ?ordering=campo o ?ordering=-campo para ordenamiento
# ?page_size= para control desde el cliente


📊 Dashboards Power BI integrados

El sistema expone endpoints específicos para Power BI:


Producción por turno — OEE, throughput, eficiencia
Control de calidad — tendencias de no conformidades
Trazabilidad de lotes — desde MP hasta despacho
Comparativo histórico — semana a semana, mes a mes



📈 Impacto medido en producción


✅ 80% reducción en tiempo de generación de reportes manuales
✅ Trazabilidad completa lote a lote en tiempo real
✅ Integración real con SAP y SCADA en planta industrial
✅ Múltiples plantas gestionadas desde una sola instancia
✅ Dashboard TV en piso de planta con KPIs en tiempo real



🚀 Instalación local (desarrollo)

bash# 1. Clonar el repositorio
git clone https://github.com/jdarangom2012/MesTostadoraLa-Central.git
cd MesTostadoraLa-Central

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Variables de entorno
cp .env.example .env
# Configurar SQL Server, SAP credentials, Azure

# 5. Migraciones (solo tablas de auth; tablas de dominio son existentes)
python manage.py migrate

# 6. Superusuario
python manage.py createsuperuser

# 7. CSS (TailwindCSS)
npm install
npm run build:css

# 8. Servidor
python manage.py runserver
# O con ASGI para WebSockets:
uvicorn mes_central.asgi:application --host 0.0.0.0 --port 8000

Variables de entorno

env# Base de datos SQL Server
DB_ENGINE=mssql
DB_NAME=agroindugestor
DB_USER=sa
DB_PASSWORD=...
DB_HOST=servidor-planta
DB_PORT=1433

# SAP
SAP_HOST=...
SAP_USER=...
SAP_PASSWORD=...

# Azure
AZURE_STORAGE_CONNECTION_STRING=...
SECRET_KEY=django-secret-key


📁 Estructura del proyecto

AgroInduGestor/
├── apps/
│   ├── produccion/     # Órdenes y seguimiento
│   ├── inventario/     # MP, insumos, PT
│   ├── calidad/        # Controles y muestreos
│   ├── trazabilidad/   # Trazabilidad lote a lote
│   ├── molienda/       # Proceso especializado cafetero
│   ├── empaque/        # Control de líneas de empaque
│   ├── reportes/       # KPIs y Power BI endpoints
│   ├── integraciones/  # SAP + SCADA + PLC
│   └── auditoria/      # Log de eventos
├── config/             # Settings Django
└── requirements.txt


🌐 Producto industrial

AgroInduGestor es un sistema MES industrial desarrollado y mantenido por NautilusTech S.A.S.

Disponible para implementación en plantas industriales de Colombia y LATAM.

📧 Contacto: admin@nautilustech.app
🌐 Web: nautilustech.app


👨‍💻 Desarrollado por

Juan David Arango Morales
Co-Founder & CTO @ NautilusTech S.A.S.
Senior Software Engineer — Python | Django | MES | SAP | SCADA

Mostrar imagen
Mostrar imagen
