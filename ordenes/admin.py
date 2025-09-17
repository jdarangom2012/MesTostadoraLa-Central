from django.contrib import admin
from .models import Orden


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado_orden', 'fecha_orden', 'fecha_entrega')
    list_filter = ('estado_orden',)
    search_fields = ('id', 'cliente__nombre')