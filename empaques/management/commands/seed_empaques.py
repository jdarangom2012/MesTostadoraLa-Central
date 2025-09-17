import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction, connection

from empaques.models import Empaque


class Command(BaseCommand):
    help = "Crea registros aleatorios de Empaques hasta completar N en total (por defecto 50)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max",
            type=int,
            default=50,
            help="Cantidad máxima total de registros a asegurar en tblEmpaques (default: 50)",
        )

    def handle(self, *args, **options):
        target_max = max(1, options.get("max") or 50)
        existing = Empaque.objects.count()
        to_create = max(0, target_max - existing)

        if to_create == 0:
            self.stdout.write(self.style.SUCCESS(f"Ya hay {existing} empaques. No se crearon nuevos registros."))
            return

        now = timezone.now()

        # Imports tolerantes: si alguna app no existe, seguimos con QS vacío
        Orden = None
        CafeEmpaque = None
        EstadoTarea = None
        try:
            from ordenes.models import Orden as _Orden
            Orden = _Orden
        except Exception:
            Orden = None
        try:
            from cafe_empaque.models import CafeEmpaque as _CafeEmpaque
            CafeEmpaque = _CafeEmpaque
        except Exception:
            CafeEmpaque = None
        try:
            from estado_tareas.models import EstadoTarea as _EstadoTarea
            EstadoTarea = _EstadoTarea
        except Exception:
            EstadoTarea = None

        ordenes_qs = Orden.objects.order_by('?') if Orden else Empaque.objects.none()
        ordenes_empaque_qs = CafeEmpaque.objects.order_by('?') if CafeEmpaque else Empaque.objects.none()
        estados_qs = EstadoTarea.objects.order_by('estado_tareas') if EstadoTarea else Empaque.objects.none()

        # Preparar filas para inserción cruda (omitimos columnas dudosas como IdOrdenEmpaque)
        rows = []
        use_estado = bool(estados_qs.exists())

        for _ in range(to_create):
            estado_id = None
            if use_estado:
                idx = random.randint(0, max(0, estados_qs.count() - 1))
                estado_id = estados_qs[idx].id

            cant_empaque = random.randint(10, 500)
            cant_empacada = random.randint(0, cant_empaque)
            cant_etiquetas = random.randint(0, 500)
            emp_clientes = random.randint(0, 50)
            total_empaques = cant_empaque
            total_paquetes = max(0, cant_empacada - random.randint(0, 10))
            total_etiquetas = max(cant_etiquetas, total_paquetes)

            fecha = now - timedelta(days=random.randint(0, 45), hours=random.randint(0, 23), minutes=random.randint(0, 59))

            rows.append({
                'FechaIngreso': fecha,
                'CantEmpaque': cant_empaque,
                'CantEmpacada': cant_empacada,
                'CantEtiquetas': cant_etiquetas,
                'EmpClientes': emp_clientes,
                'TotalEmpaques': total_empaques,
                'TotalEtiquetas': total_etiquetas,
                'TotalPaquetes': total_paquetes,
                'Notas': random.choice([None, "OK", "Revisión", "Prioridad", "Cliente solicita cambio", "Pendiente etiquetas"]),
                'created_at': fecha,
                'updated_at': fecha,
                'IdEstadoTareas': estado_id,
            })

        def insert_many(columns):
            placeholders = ','.join(['%s'] * len(columns))
            cols_sql = ','.join(f'[{c}]' for c in columns)
            sql = f"INSERT INTO [dbo].[tblEmpaques] ({cols_sql}) VALUES ({placeholders})"
            with transaction.atomic():
                with connection.cursor() as cur:
                    for row in rows:
                        params = [row.get(c) for c in columns]
                        cur.execute(sql, params)

        # Intentar con IdEstadoTareas si existe; si falla por columna inexistente, reintentar sin esa columna
        base_cols = ['FechaIngreso','CantEmpaque','CantEmpacada','CantEtiquetas','EmpClientes','TotalEmpaques','TotalEtiquetas','TotalPaquetes','Notas','created_at','updated_at']
        cols = base_cols + (['IdEstadoTareas'] if use_estado else [])
        try:
            insert_many(cols)
            used_cols = cols
        except Exception as e:
            msg = str(e)
            if 'IdEstadoTareas' in msg and 'Invalid column name' in msg:
                insert_many(base_cols)
                used_cols = base_cols
            else:
                raise

        self.stdout.write(self.style.SUCCESS(f"Se crearon {len(rows)} empaques (columnas usadas: {', '.join(used_cols)}). Total ahora: {Empaque.objects.count()}"))
