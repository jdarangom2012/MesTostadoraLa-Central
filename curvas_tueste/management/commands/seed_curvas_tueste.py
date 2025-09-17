import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from curvas_tueste.models import CurvaTueste


class Command(BaseCommand):
    help = "Llena tblCurvasTueste con registros aleatorios (máximo total especificado)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--max', type=int, default=50,
            help='Número máximo total de registros en la tabla después de sembrar (por defecto 50).'
        )

    def handle(self, *args, **options):
        max_total = max(0, int(options['max']))
        current = CurvaTueste.objects.count()
        to_create = max(0, max_total - current)

        if to_create == 0:
            self.stdout.write(self.style.WARNING(
                f'La tabla ya tiene {current} registros (máximo {max_total}). No se crean nuevos.'
            ))
            return

        now = timezone.now()
        rows = []
        for i in range(to_create):
            # Rango plausible para set point y temperatura de tueste
            temp_set = random.randint(160, 240)
            temp_tost = random.randint(140, min(temp_set, 235))
            aire = random.randint(0, 100)
            gas = random.randint(0, 100)
            # Fecha aleatoria en las últimas 6 semanas
            delta_days = random.randint(0, 42)
            delta_minutes = random.randint(0, 24 * 60)
            ts = now - timedelta(days=delta_days, minutes=delta_minutes)
            rows.append(CurvaTueste(
                fecha_ingreso=ts,
                temp_set_point=temp_set,
                temp_tost=temp_tost,
                porcentaje_aire=aire,
                porcentaje_gas=gas,
            ))

        CurvaTueste.objects.bulk_create(rows, batch_size=200)
        self.stdout.write(self.style.SUCCESS(
            f'Sembrados {to_create} registros en tblCurvasTueste (total ahora {current + to_create}).'
        ))
