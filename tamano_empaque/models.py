from django.db import models


class TamanoEmpaque(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    tamano_empaque = models.CharField(db_column='TamanoEmpaque', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblTamanoEmpaque'

    def __str__(self):
        return self.tamano_empaque or f'TamanoEmpaque {self.id}'