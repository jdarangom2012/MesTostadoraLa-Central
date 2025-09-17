from django.contrib import admin
from .models import EstadoInvenCafe


@admin.register(EstadoInvenCafe)
class EstadoInvenCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_inven_cafe')
    search_fields = ('estado_inven_cafe',)