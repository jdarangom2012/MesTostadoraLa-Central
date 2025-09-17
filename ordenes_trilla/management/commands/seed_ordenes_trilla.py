import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ordenes_trilla.models import OrdenTrilla
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea


class Command(BaseCommand):
    help = "Crea registros aleatorios de Órdenes de Trilla hasta completar 50 en total."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max",
            type=int,
            default=50,
            help="Cantidad máxima total de registros a asegurar en tblOrdenesTrilla (default: 50)",
        )

    def handle(self, *args, **options):
        target_max = max(1, options.get("max") or 50)
        existing = OrdenTrilla.objects.count()
        to_create = max(0, target_max - existing)

        if to_create == 0:
            self.stdout.write(self.style.SUCCESS(f"Ya hay {existing} órdenes de trilla. No se crearon nuevos registros."))
            return

        # Query bases
        ordenes_qs = Orden.objects.order_by('?')  # random order selection
        estados_qs = EstadoTarea.objects.order_by('estado_tareas')

        now = timezone.now()
        created = []
        for i in range(to_create):
            orden = None
            if ordenes_qs.exists():
                # tomar una orden aleatoria (no asumimos campo adicional)
                offset = random.randint(0, max(0, ordenes_qs.count() - 1))
                orden = ordenes_qs[offset]

            estado = None
            if estados_qs.exists():
                estado = estados_qs[random.randint(0, estados_qs.count() - 1)]

            # Pesos y rendimiento coherentes
            peso_bruto = round(random.uniform(1.0, 100.0), 1)
            peso_verde = round(random.uniform(0.5, max(0.5, peso_bruto * 0.9)), 1)
            rendimiento = round((peso_verde / peso_bruto) * 100.0, 1) if peso_bruto else 0.0

            # Fecha de ingreso: en los últimos 30 días
            dias_retro = random.randint(0, 30)
            fecha_ingreso = now - timedelta(days=dias_retro, hours=random.randint(0, 23), minutes=random.randint(0, 59))

            created.append(
                OrdenTrilla(
                    orden=orden,
                    estado_tareas=estado,
                    fecha_ingreso=fecha_ingreso,
                    peso_cafe_bruto=peso_bruto,
                    peso_cafe_verde=peso_verde,
                    rendimiento=rendimiento,
                    created_at=fecha_ingreso,
                    updated_at=fecha_ingreso,
                )
            )

        OrdenTrilla.objects.bulk_create(created)
        self.stdout.write(self.style.SUCCESS(f"Se crearon {len(created)} órdenes de trilla (total ahora: {existing + len(created)})."))
