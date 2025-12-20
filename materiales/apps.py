import os
from django.apps import AppConfig


class MaterialesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'materiales'
    path = os.path.dirname(os.path.abspath(__file__))