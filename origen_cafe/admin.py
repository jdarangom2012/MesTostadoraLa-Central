from django.contrib import admin
from .models import OrigenCafe


@admin.register(OrigenCafe)
class OrigenCafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'origen')
    search_fields = ('origen',)