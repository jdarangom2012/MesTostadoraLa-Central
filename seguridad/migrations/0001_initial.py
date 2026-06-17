from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('url', models.CharField(max_length=255)),
                ('icono', models.CharField(blank=True, max_length=120, null=True)),
                ('orden', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['orden', 'nombre', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=120, unique=True)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Permiso',
                'verbose_name_plural': 'Permisos',
                'ordering': ['codigo', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'ordering': ['nombre', 'id'],
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguridad.rol')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Usuario',
                'verbose_name_plural': 'Perfiles de Usuario',
            },
        ),
        migrations.CreateModel(
            name='RolModulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.modulo')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.rol')),
            ],
            options={
                'verbose_name': 'Rol-Módulo',
                'verbose_name_plural': 'Roles-Módulos',
            },
        ),
        migrations.CreateModel(
            name='RolPermiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permiso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.permiso')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.rol')),
            ],
            options={
                'verbose_name': 'Rol-Permiso',
                'verbose_name_plural': 'Roles-Permisos',
            },
        ),
        migrations.AddConstraint(
            model_name='rolmodulo',
            constraint=models.UniqueConstraint(fields=('rol', 'modulo'), name='uniq_rol_modulo'),
        ),
        migrations.AddConstraint(
            model_name='rolpermiso',
            constraint=models.UniqueConstraint(fields=('rol', 'permiso'), name='uniq_rol_permiso'),
        ),
    ]
