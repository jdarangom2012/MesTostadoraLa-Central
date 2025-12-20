import os
from django.apps import AppConfig


class NivelTuesteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nivel_tueste'
    path = os.path.dirname(os.path.abspath(__file__))