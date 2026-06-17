from django.db import migrations


PERMISOS_ADMIN_SEGURIDAD = [
    ('gestionar_permisos', 'Gestionar permisos del sistema'),
    ('ver_permisos', 'Ver configuración de permisos del sistema'),
]


def ensure_administrador_security_access(apps, schema_editor):
    Modulo = apps.get_model('seguridad', 'Modulo')
    Permiso = apps.get_model('seguridad', 'Permiso')
    Rol = apps.get_model('seguridad', 'Rol')
    RolModulo = apps.get_model('seguridad', 'RolModulo')
    RolPermiso = apps.get_model('seguridad', 'RolPermiso')

    rol_administrador = Rol.objects.filter(nombre__iexact='Administrador').first()
    if rol_administrador is None:
        return

    modulo_seguridad, _ = Modulo.objects.update_or_create(
        nombre='Seguridad',
        defaults={
            'url': '/seguridad/roles/',
            'icono': None,
            'orden': 900,
        },
    )
    RolModulo.objects.get_or_create(rol=rol_administrador, modulo=modulo_seguridad)

    for codigo, descripcion in PERMISOS_ADMIN_SEGURIDAD:
        permiso, _ = Permiso.objects.get_or_create(codigo=codigo, defaults={'descripcion': descripcion})
        RolPermiso.objects.get_or_create(rol=rol_administrador, permiso=permiso)


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0008_assign_programador_seguridad_module'),
    ]

    operations = [
        migrations.RunPython(ensure_administrador_security_access, migrations.RunPython.noop),
    ]