import os
from django.apps import AppConfig


class OrdenesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordenes'
    path = os.path.dirname(os.path.abspath(__file__))