from django.db import models


class TipoIdentificacion(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    tipo_identificacion = models.CharField(db_column='TipoIdentificacion', max_length=50, blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', blank=True, null=True)

    class Meta:
        db_table = 'tblTipoIdentificacion'

    def __str__(self):
        return self.tipo_identificacion or f'TipoIdentificacion {self.id}'