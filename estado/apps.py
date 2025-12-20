import os
from django.apps import AppConfig


class EstadoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estado'
    path = os.path.dirname(os.path.abspath(__file__))
