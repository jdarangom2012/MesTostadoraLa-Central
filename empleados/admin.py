from django.contrib import admin
from .models import Empleado, EstadoEmpleado


@admin.register(EstadoEmpleado)
class EstadoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('idEstadoEmpleado', 'Estado')
    search_fields = ('Estado',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'identificacion', 'nombres', 'apellidos', 'estado', 'fecha_ingreso')
    search_fields = ('identificacion', 'nombres', 'apellidos')
    list_filter = ('estado',)
