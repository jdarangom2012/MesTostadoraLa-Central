from django.db import migrations


def _add_grupo_columns_if_missing_sqlserver(apps, schema_editor):
    if schema_editor.connection.vendor != 'microsoft':
        return

    table_name = '[dbo].[TblOrdenesSeleccionVerde]'
    columns = ['Grupo1', 'Grupo2', 'Grupo3', 'Grupo4', 'Grupo5']

    with schema_editor.connection.cursor() as cursor:
        for col in columns:
            cursor.execute(
                f"""
                IF COL_LENGTH('{table_name}', '{col}') IS NULL
                BEGIN
                    ALTER TABLE {table_name} ADD [{col}] varchar(10) NULL;
                END
                """
            )


def _add_grupo_columns_if_missing_sqlite(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    table_name = 'TblOrdenesSeleccionVerde'
    columns = ['Grupo1', 'Grupo2', 'Grupo3', 'Grupo4', 'Grupo5']

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        existing = {row[1] for row in cursor.fetchall()}
        for col in columns:
            if col in existing:
                continue
            cursor.execute(f"ALTER TABLE \"{table_name}\" ADD COLUMN \"{col}\" varchar(10) NULL;")


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes_seleccion_verde', '0002_add_id_zaranda_grupos_fks'),
    ]

    operations = [
        migrations.RunPython(_add_grupo_columns_if_missing_sqlserver, migrations.RunPython.noop),
        migrations.RunPython(_add_grupo_columns_if_missing_sqlite, migrations.RunPython.noop),
    ]
