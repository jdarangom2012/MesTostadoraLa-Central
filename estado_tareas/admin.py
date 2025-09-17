from django.contrib import admin
from .models import EstadoTarea


@admin.register(EstadoTarea)
class EstadoTareaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_tareas')
    search_fields = ('estado_tareas',)