from django.contrib import admin
from .models import OrdenTrilla


@admin.register(OrdenTrilla)
class OrdenTrillaAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'peso_cafe_bruto', 'peso_cafe_verde', 'rendimiento')
    search_fields = ('id',)