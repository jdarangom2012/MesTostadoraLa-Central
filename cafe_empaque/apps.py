import os
from django.apps import AppConfig


class CafeEmpaqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe_empaque'
    path = os.path.dirname(os.path.abspath(__file__))