from django.contrib import admin
from .models import SeleccionTueste


@admin.register(SeleccionTueste)
class SeleccionTuesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'fecha_ingreso')