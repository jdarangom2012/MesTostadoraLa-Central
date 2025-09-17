from django.contrib import admin
from .models import LogEvento


@admin.register(LogEvento)
class LogEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_utc', 'tabla', 'accion', 'actor_username', 'correlation_id')
    list_filter = ('tabla', 'accion')
    search_fields = ('tabla', 'actor_username', 'clave', 'correlation_id')