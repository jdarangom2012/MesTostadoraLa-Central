from django.contrib import admin
from .models import OrdenTrilla
from clientes.models import Cliente
from estado_tareas.models import EstadoTarea


@admin.register(OrdenTrilla)
class OrdenTrillaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'orden_display',
        'cliente_display',
        'estado_display',
        'peso_cafe_bruto',
        'peso_cafe_verde',
        'rendimiento',
    )
    search_fields = ('id', 'orden__id', 'cliente__nombre', 'cliente__apellidos', 'orden__cliente__nombre', 'orden__cliente__apellidos')
    list_select_related = ('cliente', 'orden', 'estado_tareas', 'orden__cliente')

    @admin.display(description='Orden')
    def orden_display(self, obj: OrdenTrilla):
        if getattr(obj, 'orden_id', None):
            return f"Orden {obj.orden_id}"
        return '—'

    @admin.display(description='Cliente')
    def cliente_display(self, obj: OrdenTrilla):
        # Prioridad: cliente directo en OrdenTrilla; fallback: cliente de la orden.
        if getattr(obj, 'cliente_id', None):
            try:
                return str(obj.cliente) if obj.cliente else '—'
            except Cliente.DoesNotExist:
                return 'Sin cliente'

        if getattr(obj, 'orden_id', None):
            try:
                c = obj.orden.cliente
                return str(c) if c else '—'
            except Cliente.DoesNotExist:
                return 'Sin cliente'
            except Exception:
                return '—'

        return '—'

    @admin.display(description='Estado')
    def estado_display(self, obj: OrdenTrilla):
        if getattr(obj, 'estado_tareas_id', None):
            try:
                return str(obj.estado_tareas) if obj.estado_tareas else '—'
            except EstadoTarea.DoesNotExist:
                return '—'
        return '—'