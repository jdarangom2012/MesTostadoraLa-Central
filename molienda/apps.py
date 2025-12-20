import os
from django.apps import AppConfig


class MoliendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'molienda'
    path = os.path.dirname(os.path.abspath(__file__))