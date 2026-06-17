from django.db import migrations


def assign_tostador_edit_tueste_permission(apps, schema_editor):
    Rol = apps.get_model('seguridad', 'Rol')
    Permiso = apps.get_model('seguridad', 'Permiso')
    RolPermiso = apps.get_model('seguridad', 'RolPermiso')

    rol_tostador = Rol.objects.filter(nombre__iexact='Tostador').first()
    if rol_tostador is None:
        return

    permiso_editar_tueste, _ = Permiso.objects.get_or_create(
        codigo='editar_orden_tueste',
        defaults={'descripcion': 'Editar órdenes de tueste'},
    )
    RolPermiso.objects.get_or_create(rol=rol_tostador, permiso=permiso_editar_tueste)


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0005_assign_tostador_tueste_permissions'),
    ]

    operations = [
        migrations.RunPython(assign_tostador_edit_tueste_permission, migrations.RunPython.noop),
    ]