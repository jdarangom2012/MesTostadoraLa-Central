from django.db import models


class VariendadInvenCafe(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    variedad_inven_cafe = models.CharField(db_column='VariedadInvenCafe', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblVariendadInvenCafe'

    def __str__(self):
        return self.variedad_inven_cafe or f'VariendadInvenCafe {self.id}'