from django.db import models


class NivelTueste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    nivel_tueste = models.CharField(db_column='NivelTueste', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblNivelTueste'

    def __str__(self):
        return self.nivel_tueste or f'NivelTueste {self.id}'