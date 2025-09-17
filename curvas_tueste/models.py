from django.db import models


class CurvaTueste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    temp_set_point = models.IntegerField(db_column='TempSetPont', blank=True, null=True)
    temp_tost = models.IntegerField(db_column='TempTost', blank=True, null=True)
    porcentaje_aire = models.IntegerField(db_column='PorcentajeAire', blank=True, null=True)
    porcentaje_gas = models.IntegerField(db_column='PorcentajeGas', blank=True, null=True)

    class Meta:
        db_table = 'tblCurvasTueste'

    def __str__(self):
        return f'CurvaTueste {self.id}'