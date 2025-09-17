from django.contrib import admin
from .models import VariendadInvenCafe


@admin.register(VariendadInvenCafe)
class VariendadInvenCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'variedad_inven_cafe')
    search_fields = ('variedad_inven_cafe',)