from django.db import models


class EstadoInvenCafe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_inven_cafe = models.CharField(db_column='EstadoInvenCafe', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblEstadoInvenCafe'

    def __str__(self):
        return self.estado_inven_cafe or f'EstadoInvenCafe {self.id}'