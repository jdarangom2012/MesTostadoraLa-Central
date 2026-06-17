from django.db import models


class OrdenSeleccionTostado(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    # FKs según script: IdOrden, IdCafe, IdEstado (usamos nombres Python compatibles con el código actual)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    cafe = models.ForeignKey('inventario_cafe.InventarioCafe', models.SET_NULL, db_column='IdCafe', blank=True, null=True)
    # Nuevo FK solicitado: IdInvenCafe -> tblInventarioCafe(Id)
    inventario_cafe_ref = models.ForeignKey(
        'inventario_cafe.InventarioCafe',
        models.SET_NULL,
        db_column='IdInvenCafe',
        blank=True,
        null=True,
        related_name='seleccion_tostado_inven_cafe'
    )
    # Mantenemos el nombre 'estado_tareas' para minimizar cambios en vistas/templates, pero referencia a EstadoOrden
    estado_tareas = models.ForeignKey('estado_ordenes.EstadoOrden', models.SET_NULL, db_column='IdEstado', blank=True, null=True)

    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)

    # Campos de catación, mapeados a nombres de columna del script
    cat_limpieza = models.BooleanField(db_column='CatacionLimpieza', blank=True, null=True)
    cat_quaker = models.BooleanField(db_column='CatacionQuaker', blank=True, null=True)
    # Nota: el script usa 'pesoquater' (sic). Lo mapeamos exactamente.
    peso_quaker = models.FloatField(db_column='pesoquater', blank=True, null=True)

    cat_grupo1 = models.BooleanField(db_column='CatacionGrupo1', blank=True, null=True)
    desc_grupo1 = models.CharField(db_column='DescipGrupo1', max_length=100, blank=True, null=True)
    peso_grupo1 = models.FloatField(db_column='pesogrupo1', blank=True, null=True)

    cat_grupo2 = models.BooleanField(db_column='CatacionGrupo2', blank=True, null=True)
    desc_grupo2 = models.CharField(db_column='DescipGrupo2', max_length=100, blank=True, null=True)
    peso_grupo2 = models.FloatField(db_column='pesogrupo2', blank=True, null=True)

    cat_grupo3 = models.BooleanField(db_column='CatacionGrupo3', blank=True, null=True)
    desc_grupo3 = models.CharField(db_column='DescipGrupo3', max_length=100, blank=True, null=True)
    peso_grupo3 = models.FloatField(db_column='pesogrupo3', blank=True, null=True)

    notas = models.CharField(db_column='notas', max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblselecciontostado'

    def __str__(self):
        return f'Selección Tostado {self.id}'
