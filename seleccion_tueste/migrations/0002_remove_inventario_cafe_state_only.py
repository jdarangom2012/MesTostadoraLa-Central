from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('seleccion_tueste', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='selecciontueste',
                    name='inventario_cafe',
                ),
            ],
            database_operations=[],
        ),
    ]
