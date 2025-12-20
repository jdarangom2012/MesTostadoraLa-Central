import os
from django.apps import AppConfig


class LogEventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_eventos'
    path = os.path.dirname(os.path.abspath(__file__))