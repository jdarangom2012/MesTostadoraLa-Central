from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tueste', '0005_remove_tueste_inventario_cafe_estado'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name='tueste',
                    name='fecha_hora_inicio',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='consumo_gas',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='consumo_kwh',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='temp_deshidratacion',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='tiempo_deshidratacion',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='temp1_crack',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='tiempo1_crack',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='temp_fin_curva',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='tiempo_fin_curva',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='fecha_hora_fin',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='tempo_tueste',
                ),
                migrations.RemoveField(
                    model_name='tueste',
                    name='tiempo_enfriamiento',
                ),
            ],
        ),
    ]
