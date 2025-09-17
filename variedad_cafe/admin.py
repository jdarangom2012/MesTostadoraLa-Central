from django.contrib import admin
from .models import VariedadCafe


@admin.register(VariedadCafe)
class VariedadCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'variedad_cafe')
    search_fields = ('variedad_cafe',)