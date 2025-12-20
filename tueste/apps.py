import os
from django.apps import AppConfig


class TuesteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tueste'
    path = os.path.dirname(os.path.abspath(__file__))