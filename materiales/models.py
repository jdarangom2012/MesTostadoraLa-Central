from django.db import models


class Material(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cliente = models.ForeignKey('clientes.Cliente', models.SET_NULL, db_column='IdClientes', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    codigo_material = models.CharField(db_column='CodigoMaterial', max_length=20, blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=20, blank=True, null=True)
    cantidad = models.IntegerField(db_column='Cantidad', blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblMateriales'

    def __str__(self):
        return self.descripcion or f'Material {self.id}'