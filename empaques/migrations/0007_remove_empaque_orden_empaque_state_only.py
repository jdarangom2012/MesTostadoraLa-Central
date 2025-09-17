from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('empaques', '0006_alter_empaque_tamano'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='empaque',
                    name='orden_empaque',
                ),
            ],
            database_operations=[],
        )
    ]
