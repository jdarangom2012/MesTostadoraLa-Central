from django.db import models


class ZarandaGrupo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    zaranda_grupo = models.CharField(db_column='ZarandaGrupo', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblZarandaGrupo'

    def __str__(self):
        return self.zaranda_grupo or f'ZarandaGrupo {self.id}'