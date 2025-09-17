from django.db import models


class EstadoCliente(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_cliente = models.CharField(db_column='EstadoCliente', max_length=35, blank=True, null=True)

    class Meta:
        db_table = 'tblEstadosClientes'

    def __str__(self):
        return self.estado_cliente or f'EstadoCliente {self.id}'