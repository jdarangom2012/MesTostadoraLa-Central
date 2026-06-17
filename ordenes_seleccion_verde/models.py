from django.db import models


class OrdenSeleccionVerde(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    zaranda = models.BooleanField(db_column='Zaranda', blank=True, null=True)

    orden = models.ForeignKey(
        'ordenes.Orden',
        on_delete=models.SET_NULL,
        db_column='IdOrden',
        null=True,
        blank=True,
        db_constraint=False,
    )

    IdZarandaGrupo1 = models.ForeignKey(
        'zaranda_grupo.ZarandaGrupo',
        on_delete=models.SET_NULL,
        db_column='IdZarandaGrupo1',
        null=True,
        blank=True,
        related_name='+',
        db_constraint=False,
    )
    IdZarandaGrupo2 = models.ForeignKey(
        'zaranda_grupo.ZarandaGrupo',
        on_delete=models.SET_NULL,
        db_column='IdZarandaGrupo2',
        null=True,
        blank=True,
        related_name='+',
        db_constraint=False,
    )
    IdZarandaGrupo3 = models.ForeignKey(
        'zaranda_grupo.ZarandaGrupo',
        on_delete=models.SET_NULL,
        db_column='IdZarandaGrupo3',
        null=True,
        blank=True,
        related_name='+',
        db_constraint=False,
    )
    IdZarandaGrupo4 = models.ForeignKey(
        'zaranda_grupo.ZarandaGrupo',
        on_delete=models.SET_NULL,
        db_column='IdZarandaGrupo4',
        null=True,
        blank=True,
        related_name='+',
        db_constraint=False,
    )
    IdZarandaGrupo5 = models.ForeignKey(
        'zaranda_grupo.ZarandaGrupo',
        on_delete=models.SET_NULL,
        db_column='IdZarandaGrupo5',
        null=True,
        blank=True,
        related_name='+',
        db_constraint=False,
    )

    grupo1 = models.CharField(db_column='Grupo1', max_length=10, blank=True, null=True)
    peso_grupo1 = models.FloatField(db_column='PesoGrupo1', blank=True, null=True)
    grupo2 = models.CharField(db_column='Grupo2', max_length=10, blank=True, null=True)
    peso_grupo2 = models.FloatField(db_column='PesoGrupo2', blank=True, null=True)
    grupo3 = models.CharField(db_column='Grupo3', max_length=10, blank=True, null=True)
    peso_grupo3 = models.FloatField(db_column='PesoGrupo3', blank=True, null=True)
    grupo4 = models.CharField(db_column='Grupo4', max_length=10, blank=True, null=True)
    peso_grupo4 = models.FloatField(db_column='PesoGrupo4', blank=True, null=True)
    grupo5 = models.CharField(db_column='Grupo5', max_length=10, blank=True, null=True)
    peso_grupo5 = models.FloatField(db_column='PesoGrupo5', blank=True, null=True)
    peso_grupo_ripio = models.FloatField(db_column='PesoGrupoRipio', blank=True, null=True)
    catadora = models.BooleanField(db_column='Catadora', blank=True, null=True)
    catacion_ripio = models.BooleanField(db_column='CatacionRipio', blank=True, null=True)
    peso_cat_ripio = models.FloatField(db_column='PesoCatRipio', blank=True, null=True)
    catacion_balsos = models.BooleanField(db_column='CatacionBalsos', blank=True, null=True)
    peso_cat_balsos = models.FloatField(db_column='PesoCatBalsos', blank=True, null=True)
    catacion_grupo1 = models.BooleanField(db_column='CatacionGrupo1', blank=True, null=True)
    peso_cat_grupo1 = models.FloatField(db_column='PesoCatGrupo1', blank=True, null=True)
    catacion_grupo2 = models.BooleanField(db_column='CatacionGrupo2', blank=True, null=True)
    peso_cat_grupo2 = models.FloatField(db_column='PesoCatGrupo2', blank=True, null=True)
    peso_aceptado = models.FloatField(db_column='PesoAceptado', blank=True, null=True)
    medir_humedad = models.BooleanField(db_column='MedirHumedad', blank=True, null=True)
    humedad = models.FloatField(db_column='Humedad', blank=True, null=True)
    medir_densidad = models.BooleanField(db_column='MedirDensidad', blank=True, null=True)
    densidad = models.FloatField(db_column='Densidad', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'TblOrdenesSeleccionVerde'

    def __str__(self):
        return f'Selección Verde {self.id}'