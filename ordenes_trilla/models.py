from django.db import models
from django.db.models.functions import Now

class OrdenTrilla(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True, db_default=Now())
    cliente = models.ForeignKey('clientes.Cliente', models.SET_NULL, db_column='IdCliente', blank=True, null=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    peso_cafe_bruto = models.FloatField(db_column='PesoCafeBruto', blank=True, null=True)
    peso_cafe_verde = models.FloatField(db_column='PesoCafeVerde', blank=True, null=True)
    rendimiento = models.FloatField(db_column='Rendimiento', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblOrdenesTrilla'

    def __str__(self):
        return f'Trilla {self.id}'