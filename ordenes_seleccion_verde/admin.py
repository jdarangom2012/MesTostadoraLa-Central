from django.contrib import admin
from .models import OrdenSeleccionVerde


@admin.register(OrdenSeleccionVerde)
class OrdenSeleccionVerdeAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_tareas', 'fecha_ingreso', 'humedad', 'densidad')
    search_fields = ('id',)