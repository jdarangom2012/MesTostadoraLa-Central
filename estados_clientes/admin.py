from django.contrib import admin
from .models import EstadoCliente


@admin.register(EstadoCliente)
class EstadoClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_cliente')
    search_fields = ('estado_cliente',)