from django.db import models


class NivelMolienda(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    nivel_molienda = models.CharField(db_column='NivelMolienta', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblNivelMolienda'

    def __str__(self):
        return self.nivel_molienda or f'NivelMolienda {self.id}'