from django.contrib import admin
from .models import OrdenSeleccionTostado


@admin.register(OrdenSeleccionTostado)
class OrdenSeleccionTostadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_tareas', 'cat_limpieza', 'cat_quaker', 'peso_quaker', 'created_at')
    search_fields = ('id', 'desc_grupo1', 'desc_grupo2', 'desc_grupo3')
    list_filter = ('estado_tareas', 'cat_limpieza', 'cat_quaker')
