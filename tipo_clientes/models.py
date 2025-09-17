from django.db import models


class TipoCliente(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    tipo_cliente = models.CharField(db_column='TipoCliente', max_length=35, blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', blank=True, null=True)

    class Meta:
        db_table = 'tblTipoClientes'

    def __str__(self):
        return self.tipo_cliente or f'TipoCliente {self.id}'