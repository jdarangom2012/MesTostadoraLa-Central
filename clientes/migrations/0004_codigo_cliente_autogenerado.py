from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('clientes', '0003_cliente_representante_legal'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
-- 1) Asegurar longitud suficiente
IF COL_LENGTH('dbo.tblClientes', 'CodigoCliente') < 9
BEGIN
    ALTER TABLE dbo.tblClientes ALTER COLUMN CodigoCliente VARCHAR(9) NULL;
END;

-- 2) Crear secuencia si no existe
IF NOT EXISTS (SELECT 1 FROM sys.sequences WHERE name = 'Seq_CodigoCliente' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    DECLARE @start BIGINT = ISNULL(
        (SELECT TRY_CAST(RIGHT(CodigoCliente,6) AS INT) FROM dbo.tblClientes WHERE CodigoCliente IS NOT NULL
         ORDER BY TRY_CAST(RIGHT(CodigoCliente,6) AS INT) DESC OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY), 0) + 1;

    DECLARE @sql NVARCHAR(MAX) = N'CREATE SEQUENCE dbo.Seq_CodigoCliente AS BIGINT START WITH ' + CAST(@start AS NVARCHAR(20)) + N' INCREMENT BY 1;';
    EXEC sp_executesql @sql;
END;

-- 3) DEFAULT autoformateado con la secuencia
DECLARE @df NVARCHAR(128);
SELECT @df = d.name
FROM sys.default_constraints d
JOIN sys.columns c ON c.default_object_id = d.object_id
JOIN sys.tables t ON t.object_id = c.object_id
WHERE t.name='tblClientes' AND c.name='CodigoCliente';
IF @df IS NOT NULL
BEGIN
    EXEC('ALTER TABLE dbo.tblClientes DROP CONSTRAINT [' + @df + ']');
END;

ALTER TABLE dbo.tblClientes
ADD CONSTRAINT DF_tblClientes_CodigoCliente
DEFAULT ('CL-' + RIGHT(REPLICATE('0',6) + CAST(NEXT VALUE FOR dbo.Seq_CodigoCliente AS VARCHAR(6)), 6))
FOR CodigoCliente;

-- 4) Backfill para registros existentes con NULL
;WITH x AS (
  SELECT Id, ROW_NUMBER() OVER (ORDER BY Id) AS rn
  FROM dbo.tblClientes
  WHERE CodigoCliente IS NULL
)
UPDATE c
SET CodigoCliente = 'CL-' + RIGHT(REPLICATE('0',6) + CAST(NEXT VALUE FOR dbo.Seq_CodigoCliente AS VARCHAR(6)), 6)
FROM dbo.tblClientes c
JOIN x ON x.Id = c.Id;

-- 5) Unicidad y NOT NULL
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UX_tblClientes_CodigoCliente' AND object_id = OBJECT_ID('dbo.tblClientes'))
BEGIN
    CREATE UNIQUE INDEX UX_tblClientes_CodigoCliente ON dbo.tblClientes(CodigoCliente);
END;

ALTER TABLE dbo.tblClientes ALTER COLUMN CodigoCliente VARCHAR(9) NOT NULL;
""",
            reverse_sql="""
-- Revertir: Eliminar secuencia, default y índice único
IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UX_tblClientes_CodigoCliente' AND object_id = OBJECT_ID('dbo.tblClientes'))
BEGIN
    DROP INDEX UX_tblClientes_CodigoCliente ON dbo.tblClientes;
END;
IF EXISTS (SELECT 1 FROM sys.sequences WHERE name = 'Seq_CodigoCliente' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    DROP SEQUENCE dbo.Seq_CodigoCliente;
END;
DECLARE @df NVARCHAR(128);
SELECT @df = d.name
FROM sys.default_constraints d
JOIN sys.columns c ON c.default_object_id = d.object_id
JOIN sys.tables t ON t.object_id = c.object_id
WHERE t.name='tblClientes' AND c.name='CodigoCliente';
IF @df IS NOT NULL
BEGIN
    EXEC('ALTER TABLE dbo.tblClientes DROP CONSTRAINT [' + @df + ']');
END;
ALTER TABLE dbo.tblClientes ALTER COLUMN CodigoCliente VARCHAR(8) NULL;
"""
        )
    ]
