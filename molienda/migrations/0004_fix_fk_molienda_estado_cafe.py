from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molienda', '0003_alter_molienda_estado_inven_cafe'),
        ('estado_cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblMolienda_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblMolienda] DROP CONSTRAINT [FK_tblMolienda_tblEstadoInvenCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblMolienda_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblEstadoCafe] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoCafe] ([Id]);
    ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblEstadoCafe];
END;
            """,
            reverse_sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblMolienda_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblMolienda] DROP CONSTRAINT [FK_tblMolienda_tblEstadoCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblMolienda_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblEstadoInvenCafe] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoInvenCafe] ([Id]);
    ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblEstadoInvenCafe];
END;
            """,
        ),
    ]
