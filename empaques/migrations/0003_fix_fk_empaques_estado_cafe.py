from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empaques', '0002_alter_empaque_estado_inven_cafe'),
        ('estado_cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblEstadoInvenCafe1')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques] DROP CONSTRAINT [FK_tblEmpaques_tblEstadoInvenCafe1];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblEstadoCafe] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoCafe] ([Id]);
    ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblEstadoCafe];
END;
            """,
            reverse_sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques] DROP CONSTRAINT [FK_tblEmpaques_tblEstadoCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblEmpaques_tblEstadoInvenCafe1')
BEGIN
    ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblEstadoInvenCafe1] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoInvenCafe] ([Id]);
    ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblEstadoInvenCafe1];
END;
            """,
        ),
    ]
