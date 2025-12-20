import os
from django.apps import AppConfig


class EstadoInvenCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estado_inven_cafe'
    path = os.path.dirname(os.path.abspath(__file__))