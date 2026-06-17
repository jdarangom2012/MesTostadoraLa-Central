import django.db.models.deletion
from django.db import migrations, models


def _ensure_orden_packaging_fields(apps, schema_editor):
    Orden = apps.get_model('ordenes', 'Orden')
    connection = schema_editor.connection

    if connection.vendor == 'microsoft':
        with connection.cursor() as cursor:
            cursor.execute(
                """
                IF NOT EXISTS (
                    SELECT 1
                    FROM sys.columns
                    WHERE object_id = OBJECT_ID(N'[dbo].[tblOrdenes]')
                      AND name = N'IdEmpaque'
                )
                BEGIN
                    ALTER TABLE [dbo].[tblOrdenes] ADD [IdEmpaque] int NULL;
                END;

                IF NOT EXISTS (
                    SELECT 1
                    FROM sys.columns
                    WHERE object_id = OBJECT_ID(N'[dbo].[tblOrdenes]')
                      AND name = N'IdTamanoEmpaque'
                )
                BEGIN
                    ALTER TABLE [dbo].[tblOrdenes] ADD [IdTamanoEmpaque] int NULL;
                END;

                IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblCafeEmpaque')
                BEGIN
                    ALTER TABLE [dbo].[tblOrdenes] WITH CHECK ADD CONSTRAINT [FK_tblOrdenes_tblCafeEmpaque]
                    FOREIGN KEY([IdEmpaque]) REFERENCES [dbo].[tblCafeEmpaque] ([Id]);
                    ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblCafeEmpaque];
                END;

                IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblTamanoEmpaque')
                BEGIN
                    ALTER TABLE [dbo].[tblOrdenes] WITH CHECK ADD CONSTRAINT [FK_tblOrdenes_tblTamanoEmpaque]
                    FOREIGN KEY([IdTamanoEmpaque]) REFERENCES [dbo].[tblTamanoEmpaque] ([Id]);
                    ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblTamanoEmpaque];
                END;
                """
            )
        return

    existing_columns = {
        column.name
        for column in connection.introspection.get_table_description(connection.cursor(), Orden._meta.db_table)
    }

    for field_name in ('empaque_cafe', 'tamano_empaque'):
        field = Orden._meta.get_field(field_name)
        if field.column not in existing_columns:
            schema_editor.add_field(Orden, field)


def _drop_orden_packaging_fields(apps, schema_editor):
    if schema_editor.connection.vendor == 'microsoft':
        return

    Orden = apps.get_model('ordenes', 'Orden')
    connection = schema_editor.connection
    existing_columns = {
        column.name
        for column in connection.introspection.get_table_description(connection.cursor(), Orden._meta.db_table)
    }

    for field_name in ('tamano_empaque', 'empaque_cafe'):
        field = Orden._meta.get_field(field_name)
        if field.column in existing_columns:
            schema_editor.remove_field(Orden, field)


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_empaque', '0001_initial'),
        ('ordenes', '0013_orden_proceso_inventario_cafe_orden_variedad_cafe'),
        ('tamano_empaque', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='orden',
                    name='empaque_cafe',
                    field=models.ForeignKey(blank=True, db_column='IdEmpaque', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe_empaque.cafeempaque'),
                ),
                migrations.AddField(
                    model_name='orden',
                    name='tamano_empaque',
                    field=models.ForeignKey(blank=True, db_column='IdTamanoEmpaque', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tamano_empaque.tamanoempaque'),
                ),
            ],
        ),
        migrations.RunPython(_ensure_orden_packaging_fields, _drop_orden_packaging_fields),
    ]