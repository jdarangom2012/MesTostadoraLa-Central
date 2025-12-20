import os
from django.apps import AppConfig


class EmpleadosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empleados'
    path = os.path.dirname(os.path.abspath(__file__))