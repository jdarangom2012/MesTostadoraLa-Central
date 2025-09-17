from django.contrib import admin
from .models import ZarandaGrupo


@admin.register(ZarandaGrupo)
class ZarandaGrupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'zaranda_grupo')
    search_fields = ('zaranda_grupo',)