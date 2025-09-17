from django.contrib import admin
from .models import NivelMolienda


@admin.register(NivelMolienda)
class NivelMoliendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nivel_molienda')
    search_fields = ('nivel_molienda',)