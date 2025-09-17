from django.db import models


class Molienda(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_tarea = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTarea', blank=True, null=True)
    nivel_molienda = models.ForeignKey('nivel_molienda.NivelMolienda', models.SET_NULL, db_column='IdNivelMolienda', blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    estado_inven_cafe = models.ForeignKey('estado_cafe.EstadoCafe', models.SET_NULL, db_column='IdInvenCafe', blank=True, null=True)
    peso_moler = models.FloatField(db_column='PesoMoler', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblMolienda'
        indexes = [
            models.Index(fields=['fecha'], name='idx_molienda_fecha'),
        ]

    def __str__(self):
        return f'Molienda {self.id}'