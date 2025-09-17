from django.db import models


class EstadoOrden(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_orden = models.CharField(db_column='EstadoOrden', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblEstadoOrdenes'

    def __str__(self):
        return self.estado_orden or f'EstadoOrden {self.id}'