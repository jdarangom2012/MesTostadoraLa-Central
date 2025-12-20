import os
from django.apps import AppConfig


class NivelMoliendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nivel_molienda'
    path = os.path.dirname(os.path.abspath(__file__))