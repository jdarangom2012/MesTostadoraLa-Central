from django.db import models


class EstadoTarea(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_tareas = models.CharField(db_column='EstadoTareas', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblEstadoTareas'

    def __str__(self):
        return self.estado_tareas or f'EstadoTarea {self.id}'