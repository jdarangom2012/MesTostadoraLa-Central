from django.db import migrations, models
import django.db.models.deletion


def _drop_legacy_molienda_fk_sqlserver(apps, schema_editor):
    if schema_editor.connection.vendor != 'microsoft':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblMolienda')
            BEGIN
                ALTER TABLE [dbo].[tblEmpaques] DROP CONSTRAINT [FK_tblEmpaques_tblMolienda];
            END
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ('empaques', '0010_drop_any_triggers_ref_idordenempaque'),
        ('nivel_molienda', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_drop_legacy_molienda_fk_sqlserver, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name='empaque',
                    old_name='molienda',
                    new_name='nivel_molienda',
                ),
                migrations.AlterField(
                    model_name='empaque',
                    name='nivel_molienda',
                    field=models.ForeignKey(
                        blank=True,
                        db_column='IdNivelMolienda',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='nivel_molienda.nivelmolienda',
                    ),
                ),
            ],
        ),
    ]