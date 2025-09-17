from django.db import migrations


SQL_DROP_TRIGGERS = r"""
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql = @sql + N'DROP TRIGGER [' + SCHEMA_NAME(o.schema_id) + N'].[' + tr.name + N'];\n'
FROM sys.triggers AS tr
JOIN sys.objects AS o ON tr.parent_id = o.object_id
JOIN sys.sql_modules AS m ON m.object_id = tr.object_id
WHERE o.object_id = OBJECT_ID(N'dbo.tblEmpaques')
  AND m.definition LIKE N'%IdOrdenEmpaque%';

IF LEN(@sql) > 0
BEGIN
    EXEC sp_executesql @sql;
END;
"""


class Migration(migrations.Migration):
    dependencies = [
        ('empaques', '0008_drop_idordenempaque_if_exists'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_DROP_TRIGGERS,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
