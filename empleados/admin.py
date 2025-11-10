from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'identificacion', 'nombres', 'apellidos', 'estado', 'fecha_ingreso')
    search_fields = ('identificacion', 'nombres', 'apellidos')
    list_filter = ('estado',)
