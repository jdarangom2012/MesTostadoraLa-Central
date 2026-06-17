import django.db.models.deletion
from django.db import migrations, models


def _add_idorden_column_if_missing_sqlserver(apps, schema_editor):
    if schema_editor.connection.vendor != 'microsoft':
        return

    table_name = '[dbo].[TblOrdenesSeleccionVerde]'
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            f"""
            IF COL_LENGTH('{table_name}', 'IdOrden') IS NULL
            BEGIN
                ALTER TABLE {table_name} ADD [IdOrden] int NULL;
            END
            """
        )


def _add_idorden_column_if_missing_sqlite(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    table_name = 'TblOrdenesSeleccionVerde'
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        existing = {row[1] for row in cursor.fetchall()}
        if 'IdOrden' in existing:
            return
        cursor.execute(f"ALTER TABLE \"{table_name}\" ADD COLUMN \"IdOrden\" integer NULL;")


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0001_initial'),
        ('ordenes_seleccion_verde', '0003_add_legacy_grupo_columns'),
    ]

    operations = [
        migrations.RunPython(_add_idorden_column_if_missing_sqlserver, migrations.RunPython.noop),
        migrations.RunPython(_add_idorden_column_if_missing_sqlite, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='orden',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdOrden',
                        db_constraint=False,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='ordenes.orden',
                    ),
                ),
            ],
        ),
    ]
