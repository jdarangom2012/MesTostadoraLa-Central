import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connections
from django.conf import settings
from django.forms.models import model_to_dict
from .middleware import correlation_id_ctx, current_user_ctx

AUDIT_EXCLUDE_APPS = {'log_eventos', 'admin', 'contenttypes', 'sessions', 'auth'}


def _insert_log(tabla: str, accion: str, clave: str, datos: dict):
    try:
        user = current_user_ctx.get()
        correlation_id = correlation_id_ctx.get()
        with connections['default'].cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dbo.tblLogEventos
                (FechaUtc, Tabla, Accion, Clave, ActorUserId, ActorUsername, Source, CorrelationId, Datos, AppName)
                VALUES (sysutcdatetime(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    tabla,
                    accion,
                    clave,
                    getattr(user, 'id', None),
                    getattr(user, 'username', None),
                    'django-signal',
                    str(correlation_id) if correlation_id else None,
                    json.dumps(datos, default=str),
                    getattr(settings, 'APP_NAME', 'mes-app'),
                ]
            )
    except Exception:  # noqa: E722
        # Fallback: avoid raising inside signal
        import logging
        logging.getLogger(__name__).exception('Fallo insert auditoría')


@receiver(post_save)
def post_save_audit(sender, instance, created, **kwargs):
    app_label = getattr(sender._meta, 'app_label', '')
    if app_label in AUDIT_EXCLUDE_APPS:
        return
    if not getattr(settings, 'DEBUG', True) and sender.__name__ == 'LogEvento':
        return
    accion = 'I' if created else 'U'
    tabla = sender._meta.db_table
    clave = str(getattr(instance, 'pk', None))
    datos = model_to_dict(instance)
    _insert_log(tabla, accion, clave, datos)


@receiver(post_delete)
def post_delete_audit(sender, instance, **kwargs):
    app_label = getattr(sender._meta, 'app_label', '')
    if app_label in AUDIT_EXCLUDE_APPS:
        return
    if sender.__name__ == 'LogEvento':
        return
    tabla = sender._meta.db_table
    clave = str(getattr(instance, 'pk', None))
    datos = {'deleted': True}
    _insert_log(tabla, 'D', clave, datos)