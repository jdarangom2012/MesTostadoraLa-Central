from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0003_permisocampo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permisocampo',
            name='puede_editar',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='permisocampo',
            name='puede_ver',
            field=models.BooleanField(default=True),
        ),
    ]
