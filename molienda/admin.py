from django.contrib import admin
from .models import Molienda


@admin.register(Molienda)
class MoliendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'nivel_molienda', 'fecha', 'peso_moler')