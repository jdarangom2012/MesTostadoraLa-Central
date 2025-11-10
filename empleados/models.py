from django.db import models

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    fecha_ingreso = models.DateTimeField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        managed = True
        db_table = 'tblEmpleados'
