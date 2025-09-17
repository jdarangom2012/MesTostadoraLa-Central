from django.db import models


class EstadoCafe(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    estado_cafe = models.CharField(db_column='EstadoCafe', max_length=35, blank=True, null=True)

    class Meta:
        db_table = 'tblEstadoCafe'

    def __str__(self):
        return self.estado_cafe or f'EstadoCafe {self.id}'