import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from ordenes_seleccion_tostado.models import OrdenSeleccionTostado
from estado_ordenes.models import EstadoOrden
from ordenes.models import Orden
from inventario_cafe.models import InventarioCafe


class Command(BaseCommand):
    help = 'Crea hasta 50 registros aleatorios para tblselecciontostado'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Cantidad a crear (máx 50)')

    def handle(self, *args, **options):
        count = min(max(options['count'], 1), 50)
        estados = list(EstadoOrden.objects.all())
        if not estados:
            self.stdout.write(self.style.WARNING('No hay EstadoOrden; creando 1 por defecto'))
            estados = [EstadoOrden.objects.create(estado_orden='Pendiente')]

        ordenes = list(Orden.objects.all())
        cafes = list(InventarioCafe.objects.all())

        created = 0
        for _ in range(count):
            estado = random.choice(estados)
            cat_limpieza = random.choice([True, False])
            cat_quaker = random.choice([True, False])
            peso_quaker = round(random.uniform(0, 10), 2) if cat_quaker else 0.0
            cat_g1 = random.choice([True, False])
            cat_g2 = random.choice([True, False])
            cat_g3 = random.choice([True, False])
            now = timezone.now()
            OrdenSeleccionTostado.objects.create(
                orden=random.choice(ordenes) if ordenes else None,
                cafe=random.choice(cafes) if cafes else None,
                estado_tareas=estado,
                fecha_ingreso=now,
                cat_limpieza=cat_limpieza,
                cat_quaker=cat_quaker,
                peso_quaker=peso_quaker,
                cat_grupo1=cat_g1,
                desc_grupo1='G1' if cat_g1 else None,
                peso_grupo1=round(random.uniform(0, 50), 2) if cat_g1 else None,
                cat_grupo2=cat_g2,
                desc_grupo2='G2' if cat_g2 else None,
                peso_grupo2=round(random.uniform(0, 50), 2) if cat_g2 else None,
                cat_grupo3=cat_g3,
                desc_grupo3='G3' if cat_g3 else None,
                peso_grupo3=round(random.uniform(0, 50), 2) if cat_g3 else None,
                created_at=now,
                updated_at=now,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Creados {created} registros de Selección Tostado'))
