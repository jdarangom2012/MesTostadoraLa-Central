import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from materiales.models import Material
from clientes.models import Cliente


DESCRIPCIONES = [
    "Filtro de papel", "Etiqueta dorada", "Válvula desgasificadora",
    "Bolsa kraft 250g", "Bolsa kraft 1kg", "Caja cartón 24u",
    "Tapa plástica", "Sticker lote", "Cinta adhesiva",
    "Tarjeta QR", "Manual usuario", "Display mesa",
]


class Command(BaseCommand):
    help = "Crea hasta 50 materiales aleatorios para pruebas."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Cantidad máxima a crear (<=50)')
        parser.add_argument('--force', action='store_true', help='Ignora el límite existente y completa hasta count')

    def handle(self, *args, **opts):
        max_count = min(max(1, int(opts['count'])), 50)
        existing = Material.objects.count()
        to_create = max_count if opts['force'] else max(0, max_count - existing)
        if to_create <= 0:
            self.stdout.write(self.style.WARNING(f"Nada por crear. Ya hay {existing} materiales."))
            return

        clientes = list(Cliente.objects.all())
        now = timezone.now()
        created = []
        for i in range(to_create):
            cliente = random.choice(clientes) if clientes else None
            # Respeta longitudes de BD (descripcion max 20, codigo max 20)
            desc = random.choice(DESCRIPCIONES)[:20]
            codigo = f"MAT-{random.randint(10000, 99999)}"[:20]
            cantidad = random.randint(1, 500)
            fecha = now - timedelta(days=random.randint(0, 120))
            m = Material(
                codigo_material=codigo,
                descripcion=desc,
                cantidad=cantidad,
                estado=bool(random.getrandbits(1)),
                cliente=cliente,
                fecha_ingreso=fecha,
                created_at=fecha,
                updated_at=fecha,
            )
            created.append(m)
        Material.objects.bulk_create(created)
        self.stdout.write(self.style.SUCCESS(f"Creados {len(created)} materiales (hasta máximo {max_count})."))
