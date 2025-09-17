from django.db import models


class CafeEmpaque(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    empaque_cafe = models.CharField(db_column='EmpaqueCafe', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblCafeEmpaque'

    def __str__(self):
        return self.empaque_cafe or f'CafeEmpaque {self.id}'