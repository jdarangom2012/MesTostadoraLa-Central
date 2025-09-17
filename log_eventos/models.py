from django.db import models


class LogEvento(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)
    fecha_utc = models.DateTimeField(db_column='FechaUtc')
    tabla = models.CharField(db_column='Tabla', max_length=128)
    accion = models.CharField(db_column='Accion', max_length=1)
    clave = models.CharField(db_column='Clave', max_length=200)
    actor_user_id = models.IntegerField(db_column='ActorUserId', blank=True, null=True)
    actor_username = models.CharField(db_column='ActorUsername', max_length=150, blank=True, null=True)
    source = models.CharField(db_column='Source', max_length=50, blank=True, null=True)
    correlation_id = models.UUIDField(db_column='CorrelationId', blank=True, null=True)
    datos = models.TextField(db_column='Datos', blank=True, null=True)
    app_name = models.CharField(db_column='AppName', max_length=128, blank=True, null=True)
    host = models.CharField(db_column='Host', max_length=128, blank=True, null=True)
    usuario_sql = models.CharField(db_column='UsuarioSQL', max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'tblLogEventos'
        verbose_name = 'Log de Evento'
        verbose_name_plural = 'Log de Eventos'

    def __str__(self):
        return f'{self.id} {self.tabla} {self.accion}'