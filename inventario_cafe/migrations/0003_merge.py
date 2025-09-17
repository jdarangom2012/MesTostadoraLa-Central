from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_cafe', '0002_inventariocafe_idx_inv_codigo_and_more'),
        ('inventario_cafe', '0002_rename_empaque_to_empaquecafe'),
    ]

    operations = [
        # Solo merge; no operaciones adicionales.
    ]
