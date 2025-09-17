from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0003_alter_orden_estado_inven_cafe'),
        ('estado_cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblOrdenes] DROP CONSTRAINT [FK_tblOrdenes_tblEstadoInvenCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenes_tblEstadoCafe] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoCafe] ([Id]);
    ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblEstadoCafe];
END;
            """,
            reverse_sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblEstadoCafe')
BEGIN
    ALTER TABLE [dbo].[tblOrdenes] DROP CONSTRAINT [FK_tblOrdenes_tblEstadoCafe];
END;

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_tblOrdenes_tblEstadoInvenCafe')
BEGIN
    ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenes_tblEstadoInvenCafe] FOREIGN KEY([IdInvenCafe])
    REFERENCES [dbo].[tblEstadoInvenCafe] ([Id]);
    ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblEstadoInvenCafe];
END;
            """,
        ),
    ]
