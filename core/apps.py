import os
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    path = os.path.dirname(os.path.abspath(__file__))

    def ready(self):
        # Import signals to register handlers
        from . import signals  # noqa: F401
        # Ensure auth groups exist after migrations
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group

        # Lazy import of permission assignment helper
        def _assign_permissions():
            try:
                from .roles import assign_role_permissions
                assign_role_permissions()
            except Exception:  # noqa: E722
                import logging
                logging.getLogger(__name__).exception("No se pudieron asignar permisos a roles")

        def create_roles(sender, **kwargs):
            for name in ["admin", "operador", "coordinador"]:
                Group.objects.get_or_create(name=name)
            _assign_permissions()

        post_migrate.connect(create_roles, sender=self)
