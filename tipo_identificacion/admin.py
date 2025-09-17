from django.contrib import admin
from .models import TipoIdentificacion


@admin.register(TipoIdentificacion)
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_identificacion', 'estado')
    search_fields = ('tipo_identificacion',)