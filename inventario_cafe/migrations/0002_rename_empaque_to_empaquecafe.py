from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_empaque', '0001_initial'),
        ('inventario_cafe', '0001_initial'),
    ]

    operations = [
        # 1) Quitar FK antigua en DB (SQL Server) si existe y renombrar la columna física
        migrations.RunSQL(
            sql=(
                "IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblEmpaques') \n"
                "  ALTER TABLE [dbo].[tblInventarioCafe] DROP CONSTRAINT [FK_tblInventarioCafe_tblEmpaques];\n"
                "IF EXISTS (SELECT 1 FROM sys.columns WHERE Name = 'IdEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe'))\n"
                "  EXEC sp_rename 'dbo.tblInventarioCafe.IdEmpaque', 'IdCafeEmpaque', 'COLUMN';\n"
            ),
            reverse_sql=(
                "IF EXISTS (SELECT 1 FROM sys.columns WHERE Name = 'IdCafeEmpaque' AND Object_ID = Object_ID('dbo.tblInventarioCafe'))\n"
                "  EXEC sp_rename 'dbo.tblInventarioCafe.IdCafeEmpaque', 'IdEmpaque', 'COLUMN';\n"
            ),
        ),

        # 2) Renombrar el campo solo en el estado de Django (la DB ya se renombró arriba)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name='inventariocafe',
                    old_name='empaque',
                    new_name='empaquecafe',
                ),
            ],
        ),

        # 3) Alterar el tipo de FK y el db_column SOLO EN EL ESTADO (evitar operación DB automática)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='inventariocafe',
                    name='empaquecafe',
                    field=models.ForeignKey(blank=True, null=True, db_column='IdCafeEmpaque', on_delete=django.db.models.deletion.SET_NULL, to='cafe_empaque.cafeempaque'),
                ),
            ],
        ),

        # 4) Crear la nueva FK a tblCafeEmpaque si no existe
        migrations.RunSQL(
            sql=(
                "IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')\n"
                "  ALTER TABLE [dbo].[tblInventarioCafe] WITH CHECK ADD CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque] FOREIGN KEY([IdCafeEmpaque]) REFERENCES [dbo].[tblCafeEmpaque]([Id]);\n"
                "IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')\n"
                "  ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque];\n"
            ),
            reverse_sql=(
                "IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblInventarioCafe_tblCafeEmpaque')\n"
                "  ALTER TABLE [dbo].[tblInventarioCafe] DROP CONSTRAINT [FK_tblInventarioCafe_tblCafeEmpaque];\n"
            ),
        ),
    ]
