from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


class Tueste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    orden = models.ForeignKey('ordenes.Orden', models.SET_NULL, db_column='IdOrden', blank=True, null=True)
    inventario_cafe_ref = models.ForeignKey('inventario_cafe.InventarioCafe', models.SET_NULL, db_column='IdInventarioCafe', blank=True, null=True)
    estado_tareas = models.ForeignKey('estado_tareas.EstadoTarea', models.SET_NULL, db_column='IdEstadoTareas', blank=True, null=True)
    nivel_tueste = models.ForeignKey('nivel_tueste.NivelTueste', models.SET_NULL, db_column='IdNivelTueste', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    batche = models.IntegerField(db_column='Batche', blank=True, null=True)
    peso_cafe_vede = models.FloatField(db_column='PesoCafeVede', blank=True, null=True)
    peso_cafe_tostado = models.FloatField(db_column='PesoCafeTostado', blank=True, null=True)
    rendimiento = models.FloatField(db_column='Rendimiento', blank=True, null=True)
    peso_cafe_vede_total = models.FloatField(db_column='PesoCafeVedeTotal', blank=True, null=True)
    peso_cafe_tostado_total = models.FloatField(db_column='PesoCafeTostadoTotal', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=40, blank=True, null=True)
    notas_op = models.CharField(db_column='NotasOp', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblTueste'
        indexes = [
            models.Index(fields=['fecha_ingreso'], name='idx_tueste_fecha'),
        ]

    def __str__(self):
        return f'Tueste {self.id}'

    def calcular_peso_cafe_tostado_total_desde_batches(self):
        if not self.pk:
            return 0.0

        total = self.batches.aggregate(total=Sum('kilos_tostado')).get('total')
        try:
            return float(total or 0)
        except (TypeError, ValueError):
            return 0.0

    def sincronizar_peso_cafe_tostado_total(self):
        self.peso_cafe_tostado_total = self.calcular_peso_cafe_tostado_total_desde_batches()
        return self.peso_cafe_tostado_total

    def save(self, *args, **kwargs):
        if self.pk:
            self.sincronizar_peso_cafe_tostado_total()
        elif self.peso_cafe_tostado_total in (None, ''):
            self.peso_cafe_tostado_total = 0

        return super().save(*args, **kwargs)


class DetalleTueste(models.Model):
    id = models.AutoField(db_column='IdDetalleTueste', primary_key=True)
    tueste = models.ForeignKey('Tueste', on_delete=models.CASCADE, db_column='IdOrdenTueste', related_name='batches')
    nivel_tueste = models.ForeignKey('nivel_tueste.NivelTueste', on_delete=models.SET_NULL, null=True, blank=True, db_column='IdNivelTueste')
    estado_orden = models.ForeignKey('estado_ordenes.EstadoOrden', on_delete=models.SET_NULL, null=True, blank=True, db_column='IdEstadoOrden')
    fecha_ingreso = models.DateTimeField(db_column='FechaIngreso', null=True, blank=True)
    numero_batch = models.IntegerField(db_column='NumeroBatche')
    kilos_verde = models.FloatField(db_column='KilosVerde', null=True, blank=True)
    kilos_tostado = models.FloatField(db_column='KilosTostado', null=True, blank=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'tblDetalleTueste'
        ordering = ['numero_batch', 'id']

    COMPLETADA_PESAJE_ERROR = 'No es posible colocar el Batch en estado Completada o En Pesaje porque Kilos Verdes o Kilos Tostado son menores o iguales a cero.'

    def __str__(self):
        return f'Batch {self.numero_batch}'

    @property
    def estado_orden_label(self):
        estado_orden = getattr(self, 'estado_orden', None)
        if estado_orden is None:
            return ''
        return (getattr(estado_orden, 'estado_orden', '') or '').strip()

    def validar_estado_orden_con_pesos(self):
        estado = self.estado_orden_label.lower()
        if estado not in {'completada', 'en pesaje'}:
            return

        kilos_verde = self.kilos_verde or 0
        kilos_tostado = self.kilos_tostado or 0
        if kilos_verde <= 0 or kilos_tostado <= 0:
            raise ValidationError(self.COMPLETADA_PESAJE_ERROR)

    def clean(self):
        super().clean()
        self.validar_estado_orden_con_pesos()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def tiene_datos(self):
        return any(
            valor not in (None, '')
            for valor in (self.nivel_tueste_id, self.estado_orden_id, self.kilos_verde, self.kilos_tostado, self.observaciones)
        )