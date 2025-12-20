import os
from django.apps import AppConfig


class EstadosClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estados_clientes'
    path = os.path.dirname(os.path.abspath(__file__))