import os
from django.apps import AppConfig


class EstadoCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estado_cafe'
    path = os.path.dirname(os.path.abspath(__file__))