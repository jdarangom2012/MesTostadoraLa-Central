from django.contrib import admin
from .models import TamanoEmpaque


@admin.register(TamanoEmpaque)
class TamanoEmpaqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'tamano_empaque')
    search_fields = ('tamano_empaque',)