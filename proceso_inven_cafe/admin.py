from django.contrib import admin
from .models import ProcesoInvenCafe


@admin.register(ProcesoInvenCafe)
class ProcesoInvenCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'proceso_inven_cafe')
    search_fields = ('proceso_inven_cafe',)