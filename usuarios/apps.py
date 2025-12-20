import os
from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    path = os.path.dirname(os.path.abspath(__file__))
    verbose_name = 'Usuarios y Roles'
