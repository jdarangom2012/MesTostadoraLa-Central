import os
from django.apps import AppConfig


class EstadoOrdenesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estado_ordenes'
    path = os.path.dirname(os.path.abspath(__file__))