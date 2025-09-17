from django.db import models


class OrigenCafe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    origen = models.CharField(db_column='Origen', max_length=80)

    class Meta:
        db_table = 'tblOrigenCafe'

    def __str__(self):
        return self.origen