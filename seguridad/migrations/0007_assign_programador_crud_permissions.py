from django.db import migrations


PERMISOS_CRUD = [
    ('ver_dashboard', 'Ver dashboard'),
    ('ver_reportes', 'Ver reportes'),
    ('ver_inventario', 'Ver inventario'),
    ('crear_inventario', 'Crear inventario'),
    ('editar_inventario', 'Editar inventario'),
    ('eliminar_inventario', 'Eliminar inventario'),
    ('ver_clientes', 'Ver clientes'),
    ('crear_clientes', 'Crear clientes'),
    ('editar_clientes', 'Editar clientes'),
    ('eliminar_clientes', 'Eliminar clientes'),
    ('ver_empleados', 'Ver empleados'),
    ('crear_empleados', 'Crear empleados'),
    ('editar_empleados', 'Editar empleados'),
    ('eliminar_empleados', 'Eliminar empleados'),
    ('ver_materiales', 'Ver materiales'),
    ('crear_materiales', 'Crear materiales'),
    ('editar_materiales', 'Editar materiales'),
    ('eliminar_materiales', 'Eliminar materiales'),
    ('ver_estados', 'Ver estados'),
    ('crear_estados', 'Crear estados'),
    ('editar_estados', 'Editar estados'),
    ('eliminar_estados', 'Eliminar estados'),
    ('ver_origenes', 'Ver orígenes'),
    ('crear_origenes', 'Crear orígenes'),
    ('editar_origenes', 'Editar orígenes'),
    ('eliminar_origenes', 'Eliminar orígenes'),
    ('ver_proceso_inventario_cafe', 'Ver procesos de inventario café'),
    ('crear_proceso_inventario_cafe', 'Crear procesos de inventario café'),
    ('editar_proceso_inventario_cafe', 'Editar procesos de inventario café'),
    ('eliminar_proceso_inventario_cafe', 'Eliminar procesos de inventario café'),
    ('ver_empaque_cafe', 'Ver empaque café'),
    ('crear_empaque_cafe', 'Crear empaque café'),
    ('editar_empaque_cafe', 'Editar empaque café'),
    ('eliminar_empaque_cafe', 'Eliminar empaque café'),
    ('ver_estado_orden', 'Ver estado orden'),
    ('crear_estado_orden', 'Crear estado orden'),
    ('editar_estado_orden', 'Editar estado orden'),
    ('eliminar_estado_orden', 'Eliminar estado orden'),
    ('ver_estado_tareas', 'Ver estado tareas'),
    ('crear_estado_tareas', 'Crear estado tareas'),
    ('editar_estado_tareas', 'Editar estado tareas'),
    ('eliminar_estado_tareas', 'Eliminar estado tareas'),
    ('ver_zaranda_grupo', 'Ver zaranda grupo'),
    ('crear_zaranda_grupo', 'Crear zaranda grupo'),
    ('editar_zaranda_grupo', 'Editar zaranda grupo'),
    ('eliminar_zaranda_grupo', 'Eliminar zaranda grupo'),
    ('ver_nivel_molienda', 'Ver nivel molienda'),
    ('crear_nivel_molienda', 'Crear nivel molienda'),
    ('editar_nivel_molienda', 'Editar nivel molienda'),
    ('eliminar_nivel_molienda', 'Eliminar nivel molienda'),
    ('ver_tamano_empaque', 'Ver tamaño empaque'),
    ('crear_tamano_empaque', 'Crear tamaño empaque'),
    ('editar_tamano_empaque', 'Editar tamaño empaque'),
    ('eliminar_tamano_empaque', 'Eliminar tamaño empaque'),
    ('ver_curvas_tueste', 'Ver curvas de tueste'),
    ('crear_curvas_tueste', 'Crear curvas de tueste'),
    ('editar_curvas_tueste', 'Editar curvas de tueste'),
    ('eliminar_curvas_tueste', 'Eliminar curvas de tueste'),
    ('ver_empaque', 'Ver empaque'),
    ('crear_empaque', 'Crear empaque'),
    ('editar_empaque', 'Editar empaque'),
    ('eliminar_empaque', 'Eliminar empaque'),
    ('ver_orden_produccion', 'Ver órdenes de producción'),
    ('crear_orden_produccion', 'Crear órdenes de producción'),
    ('editar_orden_produccion', 'Editar órdenes de producción'),
    ('eliminar_orden_produccion', 'Eliminar órdenes de producción'),
    ('ver_orden_trilla', 'Ver órdenes de trilla'),
    ('crear_orden_trilla', 'Crear órdenes de trilla'),
    ('editar_orden_trilla', 'Editar órdenes de trilla'),
    ('eliminar_orden_trilla', 'Eliminar órdenes de trilla'),
    ('ver_orden_tueste', 'Ver órdenes de tueste'),
    ('crear_orden_tueste', 'Crear órdenes de tueste'),
    ('editar_orden_tueste', 'Editar órdenes de tueste'),
    ('eliminar_orden_tueste', 'Eliminar órdenes de tueste'),
    ('ver_orden_seleccion_tueste', 'Ver órdenes selección tueste'),
    ('crear_orden_seleccion_tueste', 'Crear órdenes selección tueste'),
    ('editar_orden_seleccion_tueste', 'Editar órdenes selección tueste'),
    ('eliminar_orden_seleccion_tueste', 'Eliminar órdenes selección tueste'),
    ('ver_orden_seleccion_verde', 'Ver órdenes selección verde'),
    ('ver_ordenes_seleccion_verde', 'Ver órdenes selección verde'),
    ('crear_orden_seleccion_verde', 'Crear órdenes selección verde'),
    ('editar_orden_seleccion_verde', 'Editar órdenes selección verde'),
    ('eliminar_orden_seleccion_verde', 'Eliminar órdenes selección verde'),
    ('ver_orden_seleccion_tostado', 'Ver órdenes selección tostado'),
    ('crear_orden_seleccion_tostado', 'Crear órdenes selección tostado'),
    ('editar_orden_seleccion_tostado', 'Editar órdenes selección tostado'),
    ('eliminar_orden_seleccion_tostado', 'Eliminar órdenes selección tostado'),
]


def assign_programador_permissions(apps, schema_editor):
    Modulo = apps.get_model('seguridad', 'Modulo')
    Permiso = apps.get_model('seguridad', 'Permiso')
    Rol = apps.get_model('seguridad', 'Rol')
    RolModulo = apps.get_model('seguridad', 'RolModulo')
    RolPermiso = apps.get_model('seguridad', 'RolPermiso')

    rol_programador = Rol.objects.filter(nombre__iexact='Programador').first()
    if rol_programador is None:
        return

    permisos_por_codigo = {}
    for codigo, descripcion in PERMISOS_CRUD:
        permiso, _ = Permiso.objects.get_or_create(codigo=codigo, defaults={'descripcion': descripcion})
        permisos_por_codigo[codigo] = permiso

    RolModulo.objects.filter(rol=rol_programador).delete()
    for modulo in Modulo.objects.all():
        RolModulo.objects.get_or_create(rol=rol_programador, modulo=modulo)

    RolPermiso.objects.filter(rol=rol_programador).delete()
    for codigo, permiso in permisos_por_codigo.items():
        if codigo.startswith('ver_') or codigo.startswith('crear_'):
            RolPermiso.objects.get_or_create(rol=rol_programador, permiso=permiso)


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0006_assign_tostador_editar_orden_tueste'),
    ]

    operations = [
        migrations.RunPython(assign_programador_permissions, migrations.RunPython.noop),
    ]