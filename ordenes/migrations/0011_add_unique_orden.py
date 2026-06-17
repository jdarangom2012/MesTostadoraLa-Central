from django.db import migrations, models
from django.db.models import Count


def check_no_duplicates(apps, schema_editor):
    Orden = apps.get_model('ordenes', 'Orden')
    qs = Orden.objects.values('orden')\
        .exclude(orden__isnull=True)\
        .exclude(orden__exact='')\
        .annotate(cnt=Count('id'))\
        .filter(cnt__gt=1)
    if qs.exists():
        samples = [r['orden'] for r in qs[:10]]
        raise RuntimeError(
            'No se pueden aplicar migraciones: existen valores duplicados en tblOrdenes. ' 
            f'Ejemplos: {samples}. Elimina duplicados antes de migrar.'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0010_orden_id_inventario_cafe_and_more'),
    ]

    operations = [
        migrations.RunPython(check_no_duplicates, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='orden',
            name='orden',
            field=models.CharField(db_column='Orden', max_length=16, null=True, blank=True, unique=True),
        ),
    ]
