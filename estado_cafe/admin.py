from django.contrib import admin
from .models import EstadoCafe


@admin.register(EstadoCafe)
class EstadoCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_cafe')
    search_fields = ('estado_cafe',)