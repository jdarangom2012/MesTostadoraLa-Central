from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_empaque', '0001_initial'),
        ('empaques', '0011_empaque_nivel_molienda_state_only'),
        ('nivel_molienda', '0001_initial'),
        ('tamano_empaque', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleEmpaque',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('pedido', models.PositiveIntegerField(blank=True, db_column='Pedido', null=True)),
                ('empacado', models.PositiveIntegerField(blank=True, db_column='Empacado', null=True)),
                ('suministro', models.BooleanField(db_column='Suministro', default=False)),
                ('notas', models.CharField(blank=True, db_column='Notas', max_length=255, null=True)),
                ('empaque', models.ForeignKey(db_column='IdEmpaque', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='empaques.empaque')),
                ('empaque_cafe', models.ForeignKey(blank=True, db_column='IdEmpaqueCafe', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe_empaque.cafeempaque')),
                ('nivel_molienda', models.ForeignKey(blank=True, db_column='IdNivelMolienda', null=True, on_delete=django.db.models.deletion.SET_NULL, to='nivel_molienda.nivelmolienda')),
                ('tamano_empaque', models.ForeignKey(blank=True, db_column='IdTamanoEmpaque', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tamano_empaque.tamanoempaque')),
            ],
            options={
                'db_table': 'tblDetalleEmpaques',
                'ordering': ['id'],
            },
        ),
    ]