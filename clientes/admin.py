from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_cliente', 'nombre', 'apellidos', 'codigo', 'email')
    search_fields = ('nombre', 'apellidos', 'codigo', 'codigo_cliente', 'email')
    readonly_fields = ('codigo_cliente',)