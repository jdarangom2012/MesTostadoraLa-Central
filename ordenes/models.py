from django.db import models


class Orden(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cliente = models.ForeignKey('clientes.Cliente', models.SET_NULL, db_column='IdClientes', blank=True, null=True)
    orden = models.CharField(db_column='Orden', max_length=8, blank=True, null=True)
    # Nota: ahora este campo referencia a estado_cafe.EstadoCafe, conservando el mismo nombre y columna.
    estado_inven_cafe = models.ForeignKey('estado_cafe.EstadoCafe', models.SET_NULL, db_column='IdInvenCafe', blank=True, null=True)
    estado_orden = models.ForeignKey('estado_ordenes.EstadoOrden', models.SET_NULL, db_column='IdEstadoOrden', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    fecha_orden = models.DateTimeField(db_column='FechaOrden', blank=True, null=True)
    fecha_entrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=30, blank=True, null=True)
    trilla = models.BooleanField(db_column='Trilla', blank=True, null=True)
    selec_cafe_verde = models.BooleanField(db_column='SelecCafeVerde', blank=True, null=True)
    tueste_flag = models.BooleanField(db_column='Tueste', blank=True, null=True)
    selec_cafe_tostado = models.BooleanField(db_column='SelecCafeTostado', blank=True, null=True)
    molienda_flag = models.BooleanField(db_column='Molienda', blank=True, null=True)
    empaque_flag = models.BooleanField(db_column='Empaque', blank=True, null=True)
    conf_trilla = models.BooleanField(db_column='ConfTrilla', blank=True, null=True)
    conf_sel_verde = models.BooleanField(db_column='ConfSelVerde', blank=True, null=True)
    conf_tueste = models.BooleanField(db_column='ConfTueste', blank=True, null=True)
    conf_sel_tostado = models.BooleanField(db_column='ConfSelTostado', blank=True, null=True)
    conf_molienda = models.BooleanField(db_column='ConfMolienda', blank=True, null=True)
    conf_empaque = models.BooleanField(db_column='ConfEmpaque', blank=True, null=True)
    prioridad = models.IntegerField(db_column='Prioridad', blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblOrdenes'
        indexes = [
            models.Index(fields=['fecha_orden'], name='idx_orden_fecha'),
            models.Index(fields=['cliente'], name='idx_orden_cliente'),
            models.Index(fields=['estado_orden'], name='idx_orden_estado'),
        ]

    def __str__(self):
        if self.cliente and getattr(self.cliente, 'nombre', None):
            return f'Orden {self.id} · {self.cliente.nombre}'
        return f'Orden {self.id}'