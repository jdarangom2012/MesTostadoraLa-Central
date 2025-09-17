from django.contrib import admin
from .models import NivelTueste


@admin.register(NivelTueste)
class NivelTuesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nivel_tueste')
    search_fields = ('nivel_tueste',)