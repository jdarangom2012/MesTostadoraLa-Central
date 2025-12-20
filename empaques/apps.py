import os
from django.apps import AppConfig


class EmpaquesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empaques'
    path = os.path.dirname(os.path.abspath(__file__))