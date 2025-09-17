from django.db import models


class ProcesoInvenCafe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    proceso_inven_cafe = models.CharField(db_column='ProcesoInvenCafe', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblProcesoInvenCafe'

    def __str__(self):
        return self.proceso_inven_cafe or f'ProcesoInvenCafe {self.id}'