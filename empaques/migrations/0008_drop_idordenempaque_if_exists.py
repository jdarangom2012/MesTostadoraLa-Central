from django.db import migrations

SQL_DROP_FK_AND_COLUMN = r"""
-- Eliminar índice dependiente si existe
IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'tblEmpaques_IdOrdenEmpaque_31cebcd7')
BEGIN
    DROP INDEX [tblEmpaques_IdOrdenEmpaque_31cebcd7] ON [dbo].[tblEmpaques];
END;

-- Eliminar FK dependiente si existe
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'tblEmpaques_IdOrdenEmpaque_31cebcd7_fk_tblCafeEmpaque_Id')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques] DROP CONSTRAINT [tblEmpaques_IdOrdenEmpaque_31cebcd7_fk_tblCafeEmpaque_Id];
END;

-- Drop FK if exists
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblCafeEmpaque')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques] DROP CONSTRAINT [FK_tblEmpaques_tblCafeEmpaque];
END;

-- Drop column if exists
IF EXISTS (
    SELECT 1 FROM sys.columns
    WHERE Name = N'IdOrdenEmpaque' AND Object_ID = Object_ID(N'dbo.tblEmpaques')
)
BEGIN
    ALTER TABLE [dbo].[tblEmpaques] DROP COLUMN [IdOrdenEmpaque];
END;
"""


class Migration(migrations.Migration):
    dependencies = [
        ('empaques', '0007_remove_empaque_orden_empaque_state_only'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_DROP_FK_AND_COLUMN,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
