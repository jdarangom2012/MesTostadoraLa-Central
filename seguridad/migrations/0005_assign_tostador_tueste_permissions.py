from django.conf import settings
from django.db import migrations


def assign_tostador_tueste_permissions(apps, schema_editor):
    Rol = apps.get_model('seguridad', 'Rol')
    Permiso = apps.get_model('seguridad', 'Permiso')
    RolPermiso = apps.get_model('seguridad', 'RolPermiso')
    PerfilUsuario = apps.get_model('seguridad', 'PerfilUsuario')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')

    user_app_label, user_model_name = settings.AUTH_USER_MODEL.split('.')
    apps.get_model(user_app_label, user_model_name)

    rol_tostador = Rol.objects.filter(nombre__iexact='Tostador').first()
    if rol_tostador is None:
        return

    permiso_ver_tueste, _ = Permiso.objects.get_or_create(
        codigo='ver_orden_tueste',
        defaults={'descripcion': 'Ver órdenes de tueste'},
    )
    RolPermiso.objects.get_or_create(rol=rol_tostador, permiso=permiso_ver_tueste)

    django_perm = Permission.objects.filter(
        content_type__app_label='tueste',
        codename='view_tueste',
    ).first()
    if django_perm is None:
        return

    group_tostador = Group.objects.filter(name__iexact='Tostador').first()
    if group_tostador is not None:
        group_tostador.permissions.add(django_perm)

    perfiles_tostador = PerfilUsuario.objects.select_related('user').filter(rol=rol_tostador)
    for perfil in perfiles_tostador.iterator():
        user = getattr(perfil, 'user', None)
        if user is not None:
            user.user_permissions.add(django_perm)


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0004_alter_permisocampo_defaults'),
        ('tueste', '0007_add_inventario_cafe_ref'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(assign_tostador_tueste_permissions, migrations.RunPython.noop),
    ]