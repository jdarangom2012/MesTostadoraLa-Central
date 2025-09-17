from django.contrib import admin
from .models import Empaque


@admin.register(Empaque)
class EmpaqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_tareas', 'cant_empaque', 'cant_empacada')