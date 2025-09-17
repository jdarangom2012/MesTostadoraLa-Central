from django.db import models


class Tueste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    inventario_cafe_ref = models.ForeignKey('inventario_cafe.InventarioCafe', models.SET_NULL, db_column='IdInventarioCafe', blank=True, null=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    nivel_tueste = models.ForeignKey('nivel_tueste.NivelTueste', models.SET_NULL, db_column='IdNivelTueste', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    batche = models.IntegerField(db_column='Batche', blank=True, null=True)
    peso_cafe_vede = models.FloatField(db_column='PesoCafeVede', blank=True, null=True)
    peso_cafe_tostado = models.FloatField(db_column='PesoCafeTostado', blank=True, null=True)
    rendimiento = models.FloatField(db_column='Rendimiento', blank=True, null=True)
    peso_cafe_vede_total = models.FloatField(db_column='PesoCafeVedeTotal', blank=True, null=True)
    peso_cafe_tostado_total = models.FloatField(db_column='PesoCafeTostadoTotal', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=40, blank=True, null=True)
    notas_op = models.CharField(db_column='NotasOp', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblTueste'
        indexes = [
            models.Index(fields=['fecha_ingreso'], name='idx_tueste_fecha'),
        ]

    def __str__(self):
        return f'Tueste {self.id}'