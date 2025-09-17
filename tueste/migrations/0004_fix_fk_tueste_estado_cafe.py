from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tueste', '0003_alter_tueste_inventario_cafe_estado'),
        ('estado_cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblTueste_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblTueste] DROP CONSTRAINT [FK_tblTueste_tblEstadoInvenCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblTueste_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblEstadoCafe] FOREIGN KEY([IdInventarioCafe])
    REFERENCES [dbo].[tblEstadoCafe] ([Id]);
    ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblEstadoCafe];
END;
            """,
            reverse_sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblTueste_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblTueste] DROP CONSTRAINT [FK_tblTueste_tblEstadoCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblTueste_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblEstadoInvenCafe] FOREIGN KEY([IdInventarioCafe])
    REFERENCES [dbo].[tblEstadoInvenCafe] ([Id]);
    ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblEstadoInvenCafe];
END;
            """,
        ),
    ]
