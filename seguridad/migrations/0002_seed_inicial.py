from django.db import migrations


def seed_seguridad(apps, schema_editor):
    Rol = apps.get_model('seguridad', 'Rol')
    Permiso = apps.get_model('seguridad', 'Permiso')
    Modulo = apps.get_model('seguridad', 'Modulo')

    roles = [
        ('Administrador', 'Acceso total al sistema.'),
        ('Programador', 'Acceso técnico para configuración y soporte.'),
        ('Trillador', 'Rol operativo para órdenes de trilla.'),
        ('Tostador', 'Rol operativo para órdenes de tueste.'),
        ('Empacador', 'Rol operativo para empaques e inventario.'),
    ]

    permisos = [
        ('ver_dashboard', 'Ver el dashboard'),
        ('ver_orden_trilla', 'Ver órdenes de trilla'),
        ('crear_orden_trilla', 'Crear órdenes de trilla'),
        ('editar_orden_trilla', 'Editar órdenes de trilla'),
        ('eliminar_orden_trilla', 'Eliminar órdenes de trilla'),
        ('ver_orden_tueste', 'Ver órdenes de tueste'),
        ('ver_inventario', 'Ver inventario'),
        ('configurar_sistema', 'Configurar el sistema'),
    ]

    modulos = [
        ('Dashboard', '/dashboard/', '', 1),
        ('Órdenes Trilla', '/ordenes-trilla/listar/', '', 2),
        ('Órdenes Tueste', '/ordenes-tueste/listar/', '', 3),
        ('Inventario', '/inventario-cafe/listar/', '', 4),
        ('Configuración', '/admin/', '', 5),
    ]

    for nombre, descripcion in roles:
        Rol.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})

    for codigo, descripcion in permisos:
        Permiso.objects.get_or_create(codigo=codigo, defaults={'descripcion': descripcion})

    for nombre, url, icono, orden in modulos:
        Modulo.objects.update_or_create(
            nombre=nombre,
            defaults={'url': url, 'icono': icono or None, 'orden': orden},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_seguridad, migrations.RunPython.noop),
    ]
