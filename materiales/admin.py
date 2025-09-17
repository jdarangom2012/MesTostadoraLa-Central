from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_material', 'descripcion', 'cantidad', 'estado')
    search_fields = ('codigo_material', 'descripcion')