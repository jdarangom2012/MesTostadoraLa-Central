from django.contrib import admin
from .models import CurvaTueste


@admin.register(CurvaTueste)
class CurvaTuesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_ingreso', 'temp_tost', 'porcentaje_aire', 'porcentaje_gas')