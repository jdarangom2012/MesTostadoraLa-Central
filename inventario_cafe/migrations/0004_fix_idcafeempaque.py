from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_empaque', '0001_initial'),
        ('inventario_cafe', '0003_merge'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                """
                -- Asegurar columna IdCafeEmpaque
                IF NOT EXISTS (
                    SELECT 1 FROM sys.columns 
                    WHERE Name = 'IdCafeEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe')
                )
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] ADD [IdCafeEmpaque] INT NULL;
                END;
                """
            ),
            reverse_sql="""
                IF EXISTS (
                    SELECT 1 FROM sys.columns 
                    WHERE Name = 'IdCafeEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe')
                )
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] DROP COLUMN [IdCafeEmpaque];
                END;
            """,
        ),
        migrations.RunSQL(
            sql=(
                """
                -- Copiar datos desde IdEmpaque si ambas columnas existen
                IF EXISTS (
                    SELECT 1 FROM sys.columns 
                    WHERE Name = 'IdEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe')
                ) AND EXISTS (
                    SELECT 1 FROM sys.columns 
                    WHERE Name = 'IdCafeEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe')
                )
                BEGIN
                    EXEC sp_executesql N'UPDATE ic SET ic.IdCafeEmpaque = ic.IdEmpaque FROM [dbo].[tblInventarioCafe] ic WHERE ic.IdCafeEmpaque IS NULL;';
                END;
                """
            ),
            reverse_sql="""
                -- No-op
            """,
        ),
        migrations.RunSQL(
            sql=(
                """
                -- Eliminar FK antigua si existe
                IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblEmpaques')
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] DROP CONSTRAINT [FK_tblInventarioCafe_tblEmpaques];
                END;
                """
            ),
            reverse_sql="""
                -- No-op
            """,
        ),
        migrations.RunSQL(
            sql=(
                """
                -- Crear/activar FK nueva
                IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] WITH CHECK ADD CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque]
                    FOREIGN KEY([IdCafeEmpaque]) REFERENCES [dbo].[tblCafeEmpaque]([Id]);
                END;
                IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque];
                END;
                """
            ),
            reverse_sql=(
                """
                IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')
                BEGIN
                    ALTER TABLE [dbo].[tblInventarioCafe] DROP CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque];
                END;
                """
            ),
        ),
    ]
