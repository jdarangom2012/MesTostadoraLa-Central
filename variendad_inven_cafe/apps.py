import os
from django.apps import AppConfig


class VariendadInvenCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'variendad_inven_cafe'
    path = os.path.dirname(os.path.abspath(__file__))