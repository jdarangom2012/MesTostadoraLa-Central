import os
from django.apps import AppConfig


class OrdenesSeleccionVerdeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordenes_seleccion_verde'
    path = os.path.dirname(os.path.abspath(__file__))