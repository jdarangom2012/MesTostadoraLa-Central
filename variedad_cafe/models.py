from django.db import models


class VariedadCafe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    variedad_cafe = models.CharField(db_column='VariedadCafe', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblVariedadCafe'

    def __str__(self):
        return self.variedad_cafe or f'VariedadCafe {self.id}'