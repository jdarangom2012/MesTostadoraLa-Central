from django.db import models


class SeleccionTueste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    cat_limpieza = models.BooleanField(db_column='CatLimpieza', blank=True, null=True)
    cat_quaker = models.BooleanField(db_column='CatQuaker', blank=True, null=True)
    peso_quaker = models.FloatField(db_column='PesoQuaker', blank=True, null=True)
    cat_grupo1 = models.BooleanField(db_column='CatGrupo1', blank=True, null=True)
    desc_grupo1 = models.CharField(db_column='DescGrupo1', max_length=20, blank=True, null=True)
    peso_grupo1 = models.FloatField(db_column='PesoGrupo1', blank=True, null=True)
    cat_grupo2 = models.BooleanField(db_column='CatGrupo2', blank=True, null=True)
    desc_grupo2 = models.CharField(db_column='DescGrupo2', max_length=20, blank=True, null=True)
    peso_grupo2 = models.FloatField(db_column='PesoGrupo2', blank=True, null=True)
    cat_grupo3 = models.BooleanField(db_column='CatGrupo3', blank=True, null=True)
    desc_grupo3 = models.CharField(db_column='DescGrupo3', max_length=20, blank=True, null=True)
    peso_grupo3 = models.FloatField(db_column='PesoGrupo3', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblSeleccionTueste'

    def __str__(self):
        return f'SeleccionTueste {self.id}'