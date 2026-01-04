from .settings import *
import os

# Usar una base de datos de test alternativa para evitar conflictos
DATABASES['default']['NAME'] = os.getenv('TEST_DB_NAME', 'test_dbTostadoraCentral_autogen')
# Permitir borrado automático de la base de datos de test
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
    'MIRROR': None,
}
