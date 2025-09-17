import random
from django.core.management.base import BaseCommand
from django.utils import timezone

from ordenes_seleccion_verde.models import OrdenSeleccionVerde
from estado_tareas.models import EstadoTarea


class Command(BaseCommand):
    help = "Inserta hasta N (max 50) registros aleatorios en TblOrdenesSeleccionVerde"

    def add_arguments(self, parser):
        parser.add_argument('--max', type=int, default=50, help='Cantidad máxima de registros a insertar (máx 50)')

    def handle(self, *args, **options):
        n = options.get('max') or 50
        n = max(1, min(50, int(n)))

        count_before = OrdenSeleccionVerde.objects.count()
        self.stdout.write(self.style.NOTICE(f"Registros actuales: {count_before}"))

        estados = list(EstadoTarea.objects.all())
        if not estados:
            self.stdout.write(self.style.WARNING("No hay EstadoTarea. Cree algunos antes de sembrar."))
            return

        to_create = []
        for _ in range(n):
            estado = random.choice(estados)
            zaranda = random.choice([True, False])
            catadora = random.choice([True, False])
            cat_ripio = random.choice([True, False])
            cat_balsos = random.choice([True, False])
            cat_g1 = random.choice([True, False])
            cat_g2 = random.choice([True, False])
            medir_h = random.choice([True, False])
            medir_d = random.choice([True, False])

            def rnd_txt():
                return random.choice(['12','13','14','15','16','17','18']) if random.random()>0.3 else None
            def rnd_w():
                return round(random.uniform(0.0, 50.0), 2) if random.random()>0.4 else None

            obj = OrdenSeleccionVerde(
                estado_tareas=estado,
                fecha_ingreso=timezone.now() - timezone.timedelta(days=random.randint(0, 90)),
                zaranda=zaranda,
                grupo1=rnd_txt(), peso_grupo1=rnd_w(),
                grupo2=rnd_txt(), peso_grupo2=rnd_w(),
                grupo3=rnd_txt(), peso_grupo3=rnd_w(),
                grupo4=rnd_txt(), peso_grupo4=rnd_w(),
                grupo5=rnd_txt(), peso_grupo5=rnd_w(),
                peso_grupo_ripio=rnd_w(),
                catadora=catadora,
                catacion_ripio=cat_ripio, peso_cat_ripio=rnd_w(),
                catacion_balsos=cat_balsos, peso_cat_balsos=rnd_w(),
                catacion_grupo1=cat_g1, peso_cat_grupo1=rnd_w(),
                catacion_grupo2=cat_g2, peso_cat_grupo2=rnd_w(),
                peso_aceptado=rnd_w(),
                medir_humedad=medir_h, humedad=(round(random.uniform(8.0, 12.5),2) if medir_h else None),
                medir_densidad=medir_d, densidad=(round(random.uniform(0.5, 0.9),2) if medir_d else None),
                created_at=timezone.now(), updated_at=timezone.now(),
            )
            to_create.append(obj)

        OrdenSeleccionVerde.objects.bulk_create(to_create)

        count_after = OrdenSeleccionVerde.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Insertados: {count_after - count_before}. Total: {count_after}"))
