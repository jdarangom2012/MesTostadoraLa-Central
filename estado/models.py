from django.db import models


class Estado(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado = models.CharField(db_column='Estado', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblEstados'

    def __str__(self):
        return self.estado or f'Estado {self.id}'
