from django.db import models


class Empaque(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    molienda = models.ForeignKey('molienda.Molienda', models.SET_NULL, db_column='IdMolienda', blank=True, null=True)
    # Alinear referencia con EstadoCafe si el negocio lo requiere
    estado_inven_cafe = models.ForeignKey('estado_cafe.EstadoCafe', models.SET_NULL, db_column='IdInvenCafe', blank=True, null=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    tamano = models.ForeignKey('tamano_empaque.TamanoEmpaque', models.SET_NULL, db_column='IdTamanoEmpaque', blank=True, null=True)
    cant_empaque = models.IntegerField(db_column='CantEmpaque', blank=True, null=True)
    cant_empacada = models.IntegerField(db_column='CantEmpacada', blank=True, null=True)
    cant_etiquetas = models.IntegerField(db_column='CantEtiquetas', blank=True, null=True)
    emp_clientes = models.IntegerField(db_column='EmpClientes', blank=True, null=True)
    total_empaques = models.IntegerField(db_column='TotalEmpaques', blank=True, null=True)
    total_etiquetas = models.IntegerField(db_column='TotalEtiquetas', blank=True, null=True)
    total_paquetes = models.IntegerField(db_column='TotalPaquetes', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblEmpaques'

    def __str__(self):
        return f'Empaque {self.id}'