from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0002_seed_inicial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermisoCampo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=200)),
                ('campo', models.CharField(max_length=200)),
                ('puede_ver', models.BooleanField(default=True)),
                ('puede_editar', models.BooleanField(default=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.rol')),
            ],
            options={
                'verbose_name': 'Permiso por Campo',
                'verbose_name_plural': 'Permisos por Campo',
                'ordering': ['modelo', 'campo', 'rol_id', 'id'],
            },
        ),
        migrations.AddConstraint(
            model_name='permisocampo',
            constraint=models.UniqueConstraint(fields=('rol', 'modelo', 'campo'), name='uniq_permiso_campo'),
        ),
    ]
