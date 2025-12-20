import os
from django.apps import AppConfig


class EstadoTareasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estado_tareas'
    path = os.path.dirname(os.path.abspath(__file__))