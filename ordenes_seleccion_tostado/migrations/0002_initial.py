"""Declaración de modelo vía estado y ajuste de esquema idempotente.

Esta migración NO crea la tabla (ya existe). Declara el modelo en el
estado de Django y añade la columna `IdInvenCafe` + FK si no existe.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estado_ordenes', '0001_initial'),
        ('inventario_cafe', '0005_alter_inventariocafe_empaquecafe'),
        ('ordenes', '0004_fix_fk_orden_estado_cafe'),
        ('ordenes_seleccion_tostado', '0001_fix_autoincrement_tblselecciontostado'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # SQL real en DB: agregar columna y FK si faltan
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        """
                        IF COL_LENGTH('dbo.tblselecciontostado', 'IdInvenCafe') IS NULL
                        BEGIN
                            ALTER TABLE dbo.tblselecciontostado ADD IdInvenCafe int NULL;
                        END;

                        IF NOT EXISTS (
                            SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblSeleccionTostado_tblInventarioCafe_IdInvenCafe'
                        ) AND COL_LENGTH('dbo.tblselecciontostado', 'IdInvenCafe') IS NOT NULL
                        BEGIN
                            ALTER TABLE dbo.tblselecciontostado
                            ADD CONSTRAINT FK_tblSeleccionTostado_tblInventarioCafe_IdInvenCafe
                                FOREIGN KEY (IdInvenCafe) REFERENCES dbo.tblInventarioCafe(Id);
                        END;
                        """
                    ),
                    reverse_sql=(
                        """
                        IF EXISTS (
                            SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_tblSeleccionTostado_tblInventarioCafe_IdInvenCafe'
                        )
                        BEGIN
                            ALTER TABLE dbo.tblselecciontostado
                            DROP CONSTRAINT FK_tblSeleccionTostado_tblInventarioCafe_IdInvenCafe;
                        END;

                        IF COL_LENGTH('dbo.tblselecciontostado', 'IdInvenCafe') IS NOT NULL
                        BEGIN
                            ALTER TABLE dbo.tblselecciontostado DROP COLUMN IdInvenCafe;
                        END;
                        """
                    ),
                )
            ],
            # Estado en Django: declarar el modelo con todos los campos actuales
            state_operations=[
                migrations.CreateModel(
                    name='OrdenSeleccionTostado',
                    fields=[
                        ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                        ('fecha_ingreso', models.DateTimeField(blank=True, db_column='FechaIngreso', null=True)),
                        ('cat_limpieza', models.BooleanField(blank=True, db_column='CatacionLimpieza', null=True)),
                        ('cat_quaker', models.BooleanField(blank=True, db_column='CatacionQuaker', null=True)),
                        ('peso_quaker', models.FloatField(blank=True, db_column='pesoquater', null=True)),
                        ('cat_grupo1', models.BooleanField(blank=True, db_column='CatacionGrupo1', null=True)),
                        ('desc_grupo1', models.CharField(blank=True, db_column='DescipGrupo1', max_length=100, null=True)),
                        ('peso_grupo1', models.FloatField(blank=True, db_column='pesogrupo1', null=True)),
                        ('cat_grupo2', models.BooleanField(blank=True, db_column='CatacionGrupo2', null=True)),
                        ('desc_grupo2', models.CharField(blank=True, db_column='DescipGrupo2', max_length=100, null=True)),
                        ('peso_grupo2', models.FloatField(blank=True, db_column='pesogrupo2', null=True)),
                        ('cat_grupo3', models.BooleanField(blank=True, db_column='CatacionGrupo3', null=True)),
                        ('desc_grupo3', models.CharField(blank=True, db_column='DescipGrupo3', max_length=100, null=True)),
                        ('peso_grupo3', models.FloatField(blank=True, db_column='pesogrupo3', null=True)),
                        ('notas', models.CharField(blank=True, db_column='notas', max_length=100, null=True)),
                        ('created_at', models.DateTimeField(db_column='created_at')),
                        ('updated_at', models.DateTimeField(blank=True, db_column='updated_at', null=True)),
                        ('cafe', models.ForeignKey(blank=True, db_column='IdCafe', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario_cafe.inventariocafe')),
                        ('estado_tareas', models.ForeignKey(blank=True, db_column='IdEstado', null=True, on_delete=django.db.models.deletion.SET_NULL, to='estado_ordenes.estadoorden')),
                        ('inventario_cafe_ref', models.ForeignKey(blank=True, db_column='IdInvenCafe', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seleccion_tostado_inven_cafe', to='inventario_cafe.inventariocafe')),
                        ('orden', models.ForeignKey(blank=True, db_column='IdOrden', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ordenes.orden')),
                    ],
                    options={
                        'db_table': 'tblselecciontostado',
                    },
                ),
            ],
        )
    ]
