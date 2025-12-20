import os
from django.apps import AppConfig


class OrdenesSeleccionTostadoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordenes_seleccion_tostado'
    path = os.path.dirname(os.path.abspath(__file__))
