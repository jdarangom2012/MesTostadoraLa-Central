from django.contrib import admin
from .models import TipoCliente


@admin.register(TipoCliente)
class TipoClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_cliente', 'estado')
    search_fields = ('tipo_cliente',)