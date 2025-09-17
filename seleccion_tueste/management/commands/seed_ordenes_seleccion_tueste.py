import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from seleccion_tueste.models import SeleccionTueste
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Crea registros aleatorios de Órdenes de Selección Tueste hasta completar un máximo especificado (por defecto 50)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max",
            type=int,
            default=50,
            help="Cantidad máxima total de registros a asegurar en tblSeleccionTueste (default: 50)",
        )

    def handle(self, *args, **options):
        target_max = max(1, options.get("max") or 50)
        existing = SeleccionTueste.objects.count()
        to_create = max(0, target_max - existing)

        if to_create == 0:
            self.stdout.write(self.style.SUCCESS(f"Ya hay {existing} órdenes de selección tueste. No se crearon nuevos registros."))
            return

        ordenes_qs = Orden.objects.order_by('?')
        estados_qs = EstadoTarea.objects.order_by('estado_tareas')
        inv_qs = None

        now = timezone.now()

        n_ordenes = ordenes_qs.count()
        n_estados = estados_qs.count()
        n_inv = 0

        desc_pool = [
            "Piedras",
            "Palos",
            "Metales",
            "Cascarilla",
            "Defectos varios",
            "Lotes mezclados",
            "Triado manual",
        ]

        created_rows = []

        for _ in range(to_create):
            orden = ordenes_qs[random.randint(0, n_ordenes - 1)] if n_ordenes else None
            estado = estados_qs[random.randint(0, n_estados - 1)] if n_estados else None
            inv = None

            dias_retro = random.randint(0, 45)
            fecha_ingreso = now - timedelta(days=dias_retro, hours=random.randint(0, 23), minutes=random.randint(0, 59))

            cat_limpieza = random.choice([True, False])
            cat_quaker = random.choice([True, False])
            peso_quaker = round(random.uniform(0.0, 5.0), 2) if cat_quaker else None

            g1 = random.choice([True, False])
            g2 = random.choice([True, False])
            g3 = random.choice([True, False])

            desc1 = random.choice(desc_pool) if g1 else None
            desc2 = random.choice(desc_pool) if g2 else None
            desc3 = random.choice(desc_pool) if g3 else None

            peso1 = round(random.uniform(0.1, 10.0), 2) if g1 else None
            peso2 = round(random.uniform(0.1, 10.0), 2) if g2 else None
            peso3 = round(random.uniform(0.1, 10.0), 2) if g3 else None

            created_rows.append({
                'IdOrden': orden.id if orden else None,
                'IdEstadoTareas': estado.id if estado else None,
                # 'IdInventarioCafe' omitido (columna no utilizada)
                'FechaIngreso': fecha_ingreso,
                'CatLimpieza': cat_limpieza,
                'CatQuaker': cat_quaker,
                'PesoQuaker': peso_quaker,
                'CatGrupo1': g1,
                'DescGrupo1': desc1,
                'PesoGrupo1': peso1,
                'CatGrupo2': g2,
                'DescGrupo2': desc2,
                'PesoGrupo2': peso2,
                'CatGrupo3': g3,
                'DescGrupo3': desc3,
                'PesoGrupo3': peso3,
                'created_at': fecha_ingreso,
                'updated_at': fecha_ingreso,
            })

        # Introspect existing columns to avoid referencing non-existent ones (e.g., IdInventarioCafe)
        with connection.cursor() as cur:
            table = SeleccionTueste._meta.db_table
            desc = connection.introspection.get_table_description(cur, table)
            existing_cols = {c.name for c in desc}

        base_cols = [
            'IdOrden', 'IdEstadoTareas', 'FechaIngreso',
            'CatLimpieza', 'CatQuaker', 'PesoQuaker',
            'CatGrupo1', 'DescGrupo1', 'PesoGrupo1',
            'CatGrupo2', 'DescGrupo2', 'PesoGrupo2',
            'CatGrupo3', 'DescGrupo3', 'PesoGrupo3',
            'created_at', 'updated_at',
        ]
        # Columnas a insertar (sin IdInventarioCafe)
        columns = ['IdOrden', 'IdEstadoTareas'] + [
            'FechaIngreso', 'CatLimpieza', 'CatQuaker', 'PesoQuaker',
            'CatGrupo1', 'DescGrupo1', 'PesoGrupo1',
            'CatGrupo2', 'DescGrupo2', 'PesoGrupo2',
            'CatGrupo3', 'DescGrupo3', 'PesoGrupo3',
            'created_at', 'updated_at',
        ]

        # Filter rows to only include existing columns
        param_rows = []
        for row in created_rows:
            filtered = [row.get(col) for col in columns]
            param_rows.append(tuple(filtered))

        placeholders = ', '.join(['%s'] * len(columns))
        col_sql = ', '.join(f'[{c}]' for c in columns)
        insert_sql = f"INSERT INTO {SeleccionTueste._meta.db_table} ({col_sql}) VALUES ({placeholders})"

        with transaction.atomic():
            with connection.cursor() as cur:
                cur.executemany(insert_sql, param_rows)

        self.stdout.write(self.style.SUCCESS(f"Se crearon {len(param_rows)} órdenes de selección tueste (total ahora: {existing + len(param_rows)})."))
