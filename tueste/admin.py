from django.contrib import admin
from .models import Tueste


@admin.register(Tueste)
class TuesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'nivel_tueste', 'fecha_ingreso', 'rendimiento')