import os
from django.apps import AppConfig


class ZarandaGrupoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zaranda_grupo'
    path = os.path.dirname(os.path.abspath(__file__))