from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tueste', '0006_remove_curve_fields_state_only'),
        ('inventario_cafe', '0005_alter_inventariocafe_empaquecafe'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=r"""
IF COL_LENGTH('dbo.tblTueste', 'IdInventarioCafe') IS NULL
BEGIN
    ALTER TABLE dbo.tblTueste ADD IdInventarioCafe int NULL;
END;

IF NOT EXISTS (
    SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblTueste_tblInventarioCafe_IdInventarioCafe'
)
AND COL_LENGTH('dbo.tblTueste', 'IdInventarioCafe') IS NOT NULL
BEGIN
    ALTER TABLE dbo.tblTueste
    ADD CONSTRAINT FK_tblTueste_tblInventarioCafe_IdInventarioCafe
        FOREIGN KEY (IdInventarioCafe) REFERENCES dbo.tblInventarioCafe(Id);
END;
                    """,
                    reverse_sql=r"""
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblTueste_tblInventarioCafe_IdInventarioCafe')
BEGIN
    ALTER TABLE dbo.tblTueste DROP CONSTRAINT FK_tblTueste_tblInventarioCafe_IdInventarioCafe;
END;

IF COL_LENGTH('dbo.tblTueste', 'IdInventarioCafe') IS NOT NULL
BEGIN
    ALTER TABLE dbo.tblTueste DROP COLUMN IdInventarioCafe;
END;
                    """,
                )
            ],
            state_operations=[
                migrations.AddField(
                    model_name='tueste',
                    name='inventario_cafe_ref',
                    field=models.ForeignKey(blank=True, db_column='IdInventarioCafe', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario_cafe.inventariocafe'),
                ),
            ],
        )
    ]
