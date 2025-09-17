import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tueste.models import Tueste
from ordenes.models import Orden
from estado_tareas.models import EstadoTarea
from nivel_tueste.models import NivelTueste
# Campo IdInventarioCafe fue eliminado del modelo Tueste; no se requiere EstadoCafe aquí


class Command(BaseCommand):
    help = "Crea registros aleatorios de Órdenes de Tueste hasta completar 50 en total."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max",
            type=int,
            default=50,
            help="Cantidad máxima total de registros a asegurar en tblTueste (default: 50)",
        )

    def handle(self, *args, **options):
        target_max = max(1, options.get("max") or 50)
        existing = Tueste.objects.count()
        to_create = max(0, target_max - existing)

        if to_create == 0:
            self.stdout.write(self.style.SUCCESS(f"Ya hay {existing} órdenes de tueste. No se crearon nuevos registros."))
            return

        ordenes_qs = Orden.objects.order_by('?')
        estados_qs = EstadoTarea.objects.order_by('estado_tareas')
        niveles_qs = NivelTueste.objects.order_by('nivel_tueste')

        now = timezone.now()
        created = []
        notas_pool = [
            "Perfil claro",
            "Perfil medio",
            "Perfil oscuro",
            "Controlar ventilación",
            "Verificar primer crack",
            "Ajuste flujo gas",
            "Consistencia batch",
        ]

        n_ordenes = ordenes_qs.count()
        n_estados = estados_qs.count()
        n_niveles = niveles_qs.count()

        for _ in range(to_create):
            orden = None
            if n_ordenes:
                orden = ordenes_qs[random.randint(0, n_ordenes - 1)]

            estado_t = None
            if n_estados:
                estado_t = estados_qs[random.randint(0, n_estados - 1)]

            nivel = None
            if n_niveles:
                nivel = niveles_qs[random.randint(0, n_niveles - 1)]

            batche = random.randint(1, 5)
            peso_verde = round(random.uniform(5.0, 50.0), 2)
            factor = random.uniform(0.75, 0.95)
            peso_tostado = round(peso_verde * factor, 2)
            rendimiento = round((peso_tostado / peso_verde) * 100.0, 2) if peso_verde else 0.0

            dias_retro = random.randint(0, 30)
            fecha_ingreso = now - timedelta(days=dias_retro, hours=random.randint(0, 23), minutes=random.randint(0, 59))

            created.append(
                Tueste(
                    orden=orden,
                    estado_tareas=estado_t,
                    nivel_tueste=nivel,
                    fecha_ingreso=fecha_ingreso,
                    batche=batche,
                    peso_cafe_vede=peso_verde,
                    peso_cafe_tostado=peso_tostado,
                    rendimiento=rendimiento,
                    notas=random.choice(notas_pool),
                    created_at=fecha_ingreso,
                    updated_at=fecha_ingreso,
                )
            )

        Tueste.objects.bulk_create(created)
        self.stdout.write(self.style.SUCCESS(f"Se crearon {len(created)} órdenes de tueste (total ahora: {existing + len(created)})."))
