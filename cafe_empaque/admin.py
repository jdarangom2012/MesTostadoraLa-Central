from django.contrib import admin
from .models import CafeEmpaque


@admin.register(CafeEmpaque)
class CafeEmpaqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'empaque_cafe')
    search_fields = ('empaque_cafe',)