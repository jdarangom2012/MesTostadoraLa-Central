from django.db import migrations


UP_SQL = r"""
IF OBJECT_ID('dbo.tblSeleccionTostado', 'U') IS NOT NULL
AND ISNULL(COLUMNPROPERTY(OBJECT_ID('dbo.tblSeleccionTostado'), 'Id', 'IsIdentity'), 0) <> 1
BEGIN
    DECLARE @start int = 1 + ISNULL((SELECT MAX(Id) FROM dbo.tblSeleccionTostado WITH (HOLDLOCK, TABLOCKX)), 0);

    IF NOT EXISTS (
        SELECT 1 FROM sys.sequences
        WHERE name = 'Seq_tblSeleccionTostado' AND SCHEMA_NAME(schema_id) = 'dbo'
    )
    BEGIN
        DECLARE @sqlCreateSeq nvarchar(400);
        SET @sqlCreateSeq = N'CREATE SEQUENCE dbo.Seq_tblSeleccionTostado AS int START WITH ' + CAST(@start AS nvarchar(20)) + N' INCREMENT BY 1';
        EXEC sp_executesql @sqlCreateSeq;
    END
    ELSE
    BEGIN
        DECLARE @sqlRestartSeq nvarchar(400);
        SET @sqlRestartSeq = N'ALTER SEQUENCE dbo.Seq_tblSeleccionTostado RESTART WITH ' + CAST(@start AS nvarchar(20));
        EXEC sp_executesql @sqlRestartSeq;
    END

    IF NOT EXISTS (
        SELECT 1
        FROM sys.default_constraints dc
        JOIN sys.columns c ON c.default_object_id = dc.object_id
        JOIN sys.tables t ON t.object_id = c.object_id
        WHERE t.name = 'tblSeleccionTostado' AND SCHEMA_NAME(t.schema_id) = 'dbo' AND c.name = 'Id'
    )
    BEGIN
        ALTER TABLE dbo.tblSeleccionTostado
        ADD CONSTRAINT DF_tblSeleccionTostado_Id DEFAULT (NEXT VALUE FOR dbo.Seq_tblSeleccionTostado) FOR Id;
    END
END
"""

DOWN_SQL = r"""
IF OBJECT_ID('dbo.tblSeleccionTostado', 'U') IS NOT NULL
BEGIN
    DECLARE @dcName sysname;
    SELECT @dcName = dc.name
    FROM sys.default_constraints dc
    JOIN sys.columns c ON c.default_object_id = dc.object_id
    JOIN sys.tables t ON t.object_id = c.object_id
    WHERE t.name = 'tblSeleccionTostado' AND SCHEMA_NAME(t.schema_id) = 'dbo' AND c.name = 'Id';
    IF @dcName IS NOT NULL
    BEGIN
        DECLARE @sql nvarchar(400) = N'ALTER TABLE dbo.tblSeleccionTostado DROP CONSTRAINT ' + QUOTENAME(@dcName) + N';';
        EXEC sp_executesql @sql;
    END
END
IF EXISTS (
    SELECT 1 FROM sys.sequences
    WHERE name = 'Seq_tblSeleccionTostado' AND SCHEMA_NAME(schema_id) = 'dbo'
)
BEGIN
    DROP SEQUENCE dbo.Seq_tblSeleccionTostado;
END
"""


class Migration(migrations.Migration):
    dependencies = []

    def run_sql_if_not_test(apps, schema_editor):
        db_name = schema_editor.connection.settings_dict.get('NAME', '')
        if not db_name.startswith('test_'):
            schema_editor.execute(UP_SQL)
    def reverse_sql_if_not_test(apps, schema_editor):
        db_name = schema_editor.connection.settings_dict.get('NAME', '')
        if not db_name.startswith('test_'):
            schema_editor.execute(DOWN_SQL)
    operations = [
        migrations.RunPython(run_sql_if_not_test, reverse_code=reverse_sql_if_not_test),
    ]
