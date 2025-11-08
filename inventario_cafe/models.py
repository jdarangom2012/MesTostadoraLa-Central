from django.db import models


class InventarioCafe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cliente = models.ForeignKey('clientes.Cliente', models.SET_NULL, db_column='IdClientes', blank=True, null=True)
    estado_cafe = models.ForeignKey('estado_cafe.EstadoCafe', models.SET_NULL, db_column='IdEstadoCafe', blank=True, null=True)
    proceso_inven_cafe = models.ForeignKey('proceso_inven_cafe.ProcesoInvenCafe', models.SET_NULL, db_column='IdProcesoInvenCafe', blank=True, null=True)
    variendad_inven_cafe = models.ForeignKey('variendad_inven_cafe.VariendadInvenCafe', models.SET_NULL, db_column='IdVariendadInvenCafe', blank=True, null=True)
    origen = models.ForeignKey('origen_cafe.OrigenCafe', models.SET_NULL, db_column='IdOrigen', blank=True, null=True)
    empaquecafe = models.ForeignKey('cafe_empaque.CafeEmpaque', models.SET_NULL, db_column='IdEmpaqueCafe', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    codigo = models.CharField(db_column='Codigo', max_length=20, blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=50, blank=True, null=True)
    cantidad = models.FloatField(db_column='Cantidad', blank=True, null=True)
    sacos = models.IntegerField(db_column='Sacos', blank=True, null=True)
    cantidad_bolsas_emp = models.IntegerField(db_column='CantidadBolsasEmp', blank=True, null=True)
    cantidad_paquetes = models.IntegerField(db_column='CantidadPaquetes', blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblInventarioCafe'
        indexes = [
            models.Index(fields=['codigo'], name='idx_inv_codigo'),
            models.Index(fields=['cliente'], name='idx_inv_cliente'),
            models.Index(fields=['estado_cafe'], name='idx_inv_estado_cafe'),
        ]

    def __str__(self):
        return f'InventarioCafe {self.id}'