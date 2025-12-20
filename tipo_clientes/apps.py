import os
from django.apps import AppConfig


class TipoClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tipo_clientes'
    path = os.path.dirname(os.path.abspath(__file__))