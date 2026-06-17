from django.contrib import admin

from .models import Modulo, Permiso, PermisoCampo, PerfilUsuario, Rol, RolModulo, RolPermiso


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'url', 'orden')
    list_editable = ('orden',)
    search_fields = ('nombre', 'url')
    ordering = ('orden', 'nombre')


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')


@admin.register(RolModulo)
class RolModuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'rol', 'modulo')
    list_filter = ('rol',)
    search_fields = ('rol__nombre', 'modulo__nombre')


@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'rol', 'permiso')
    list_filter = ('rol',)
    search_fields = ('rol__nombre', 'permiso__codigo', 'permiso__descripcion')


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'rol__nombre')


@admin.register(PermisoCampo)
class PermisoCampoAdmin(admin.ModelAdmin):
    list_display = ('rol', 'modelo', 'campo', 'puede_ver', 'puede_editar')
    list_filter = ('rol', 'modelo')
    search_fields = ('campo',)
    ordering = ('rol', 'modelo', 'campo')
