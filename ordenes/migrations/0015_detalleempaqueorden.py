import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_empaque', '0001_initial'),
        ('ordenes', '0014_orden_empaque_cafe_tamano_empaque'),
        ('tamano_empaque', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleEmpaqueOrden',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(blank=True, db_column='Cantidad', null=True)),
                ('empaque_cafe', models.ForeignKey(blank=True, db_column='IdEmpaqueCafe', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe_empaque.cafeempaque')),
                ('orden', models.ForeignKey(db_column='IdOrden', on_delete=django.db.models.deletion.CASCADE, related_name='detalles_empaque', to='ordenes.orden')),
                ('tamano_empaque', models.ForeignKey(blank=True, db_column='IdTamanoEmpaque', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tamano_empaque.tamanoempaque')),
            ],
            options={
                'db_table': 'tblDetalleEmpaqueOrden',
                'ordering': ['id'],
            },
        ),
    ]