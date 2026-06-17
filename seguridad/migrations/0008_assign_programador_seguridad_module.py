from django.db import migrations


def ensure_programador_seguridad_module(apps, schema_editor):
    Modulo = apps.get_model('seguridad', 'Modulo')
    Rol = apps.get_model('seguridad', 'Rol')
    RolModulo = apps.get_model('seguridad', 'RolModulo')

    modulo_seguridad, _ = Modulo.objects.update_or_create(
        nombre='Seguridad',
        defaults={
            'url': '/seguridad/roles/',
            'icono': None,
            'orden': 900,
        },
    )

    rol_programador = Rol.objects.filter(nombre__iexact='Programador').first()
    if rol_programador is None:
        return

    RolModulo.objects.get_or_create(rol=rol_programador, modulo=modulo_seguridad)


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0007_assign_programador_crud_permissions'),
    ]

    operations = [
        migrations.RunPython(ensure_programador_seguridad_module, migrations.RunPython.noop),
    ]