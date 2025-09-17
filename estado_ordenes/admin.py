from django.contrib import admin
from .models import EstadoOrden


@admin.register(EstadoOrden)
class EstadoOrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_orden')
    search_fields = ('estado_orden',)