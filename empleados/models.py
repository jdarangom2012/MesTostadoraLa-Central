from django.db import models


class EstadoEmpleado(models.Model):
    idEstadoEmpleado = models.AutoField(primary_key=True, db_column='idEstadoEmpleado')
    Estado = models.CharField(max_length=50, db_column='Estado')

    def __str__(self):
        return str(self.Estado)

    class Meta:
        managed = False
        db_table = 'tblEstadoEmpleados'


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    estado = models.ForeignKey(
        EstadoEmpleado,
        on_delete=models.PROTECT,
        db_column='IdEstadoEmpleado',
        related_name='empleados',
    )
    fecha_ingreso = models.DateTimeField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        managed = False
        db_table = 'tblEmpleados'
