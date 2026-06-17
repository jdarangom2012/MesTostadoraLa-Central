from django.db import migrations


def fix_programador_orden_produccion_permissions(apps, schema_editor):
    Permiso = apps.get_model('seguridad', 'Permiso')
    Rol = apps.get_model('seguridad', 'Rol')
    RolPermiso = apps.get_model('seguridad', 'RolPermiso')

    rol_programador = Rol.objects.filter(nombre__iexact='Programador').first()
    if rol_programador is None:
        return

    permisos = {}
    for codigo, descripcion in [
        ('ver_orden_produccion', 'Ver órdenes de producción'),
        ('crear_orden_produccion', 'Crear órdenes de producción'),
        ('editar_orden_produccion', 'Editar órdenes de producción'),
        ('eliminar_orden_produccion', 'Eliminar órdenes de producción'),
    ]:
        permiso, _ = Permiso.objects.get_or_create(codigo=codigo, defaults={'descripcion': descripcion})
        permisos[codigo] = permiso

    for codigo in ['ver_orden_produccion', 'crear_orden_produccion']:
        RolPermiso.objects.get_or_create(rol=rol_programador, permiso=permisos[codigo])

    for codigo in ['editar_orden_produccion', 'eliminar_orden_produccion']:
        RolPermiso.objects.filter(rol=rol_programador, permiso=permisos[codigo]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0010_ensure_programador_orden_produccion_create_view'),
    ]

    operations = [
        migrations.RunPython(fix_programador_orden_produccion_permissions, migrations.RunPython.noop),
    ]