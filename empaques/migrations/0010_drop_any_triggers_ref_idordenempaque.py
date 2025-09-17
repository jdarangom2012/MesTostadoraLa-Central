from django.db import migrations


SQL_DROP_ANY_TRIGGERS = r"""
DECLARE @schema SYSNAME, @trig SYSNAME, @sql NVARCHAR(MAX);

DECLARE cur CURSOR FAST_FORWARD FOR
SELECT SCHEMA_NAME(o.schema_id) AS schema_name, tr.name AS trigger_name
FROM sys.triggers AS tr
JOIN sys.objects AS o ON tr.parent_id = o.object_id
JOIN sys.sql_modules AS m ON m.object_id = tr.object_id
WHERE m.definition LIKE N'%IdOrdenEmpaque%';

OPEN cur;
FETCH NEXT FROM cur INTO @schema, @trig;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = N'DROP TRIGGER [' + @schema + N'].[' + @trig + N']';
    BEGIN TRY
        EXEC sp_executesql @sql;
        PRINT 'Dropped trigger [' + @schema + '].[' + @trig + '] referencing IdOrdenEmpaque';
    END TRY
    BEGIN CATCH
        PRINT 'Failed dropping trigger [' + @schema + '].[' + @trig + '] : ' + ERROR_MESSAGE();
    END CATCH
    FETCH NEXT FROM cur INTO @schema, @trig;
END

CLOSE cur;
DEALLOCATE cur;
"""


class Migration(migrations.Migration):
    dependencies = [
        ('empaques', '0009_drop_triggers_ref_idordenempaque'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_DROP_ANY_TRIGGERS,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
