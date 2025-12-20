import os
from django.apps import AppConfig


class InventarioCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario_cafe'
    path = os.path.dirname(os.path.abspath(__file__))