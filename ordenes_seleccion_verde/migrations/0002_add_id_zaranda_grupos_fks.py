from django.db import migrations, models


def _add_columns_if_missing_sqlserver(apps, schema_editor):
    if schema_editor.connection.vendor != 'microsoft':
        return

    table_name = '[dbo].[TblOrdenesSeleccionVerde]'
    columns = [
        'IdZarandaGrupo1',
        'IdZarandaGrupo2',
        'IdZarandaGrupo3',
        'IdZarandaGrupo4',
        'IdZarandaGrupo5',
    ]

    with schema_editor.connection.cursor() as cursor:
        for col in columns:
            cursor.execute(
                f"""
                IF COL_LENGTH('{table_name}', '{col}') IS NULL
                BEGIN
                    ALTER TABLE {table_name} ADD [{col}] int NULL;
                END
                """
            )


def _add_columns_if_missing_sqlite(apps, schema_editor):
    # Permite que entornos SQLite (tests/dev) creen las columnas si faltan.
    if schema_editor.connection.vendor != 'sqlite':
        return

    table_name = 'TblOrdenesSeleccionVerde'
    columns = [
        'IdZarandaGrupo1',
        'IdZarandaGrupo2',
        'IdZarandaGrupo3',
        'IdZarandaGrupo4',
        'IdZarandaGrupo5',
    ]

    with schema_editor.connection.cursor() as cursor:
        for col in columns:
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            existing = {row[1] for row in cursor.fetchall()}
            if col in existing:
                continue
            cursor.execute(f"ALTER TABLE \"{table_name}\" ADD COLUMN \"{col}\" integer NULL;")


class Migration(migrations.Migration):

    dependencies = [
        ('zaranda_grupo', '0001_initial'),
        ('ordenes_seleccion_verde', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_add_columns_if_missing_sqlserver, migrations.RunPython.noop),
        migrations.RunPython(_add_columns_if_missing_sqlite, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='IdZarandaGrupo1',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdZarandaGrupo1',
                        on_delete=models.deletion.SET_NULL,
                        related_name='+',
                        db_constraint=False,
                        to='zaranda_grupo.zarandagrupo',
                    ),
                ),
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='IdZarandaGrupo2',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdZarandaGrupo2',
                        on_delete=models.deletion.SET_NULL,
                        related_name='+',
                        db_constraint=False,
                        to='zaranda_grupo.zarandagrupo',
                    ),
                ),
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='IdZarandaGrupo3',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdZarandaGrupo3',
                        on_delete=models.deletion.SET_NULL,
                        related_name='+',
                        db_constraint=False,
                        to='zaranda_grupo.zarandagrupo',
                    ),
                ),
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='IdZarandaGrupo4',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdZarandaGrupo4',
                        on_delete=models.deletion.SET_NULL,
                        related_name='+',
                        db_constraint=False,
                        to='zaranda_grupo.zarandagrupo',
                    ),
                ),
                migrations.AddField(
                    model_name='ordenseleccionverde',
                    name='IdZarandaGrupo5',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        db_column='IdZarandaGrupo5',
                        on_delete=models.deletion.SET_NULL,
                        related_name='+',
                        db_constraint=False,
                        to='zaranda_grupo.zarandagrupo',
                    ),
                ),
            ],
        ),
    ]
