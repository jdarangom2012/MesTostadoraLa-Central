import random
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.db import transaction

from ordenes.models import Orden
from clientes.models import Cliente
from estado_ordenes.models import EstadoOrden
from estado_cafe.models import EstadoCafe


class Command(BaseCommand):
    help = "Llena la tabla de órdenes de producción con un máximo de 50 registros aleatorios."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max",
            type=int,
            default=50,
            help="Cantidad máxima de órdenes totales a dejar en la tabla (se hace top-up).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        max_total: int = options["max"]

        existing = Orden.objects.count()
        to_create = max(0, max_total - existing)

        if to_create == 0:
            self.stdout.write(self.style.SUCCESS(f"No se crearon órdenes. Ya hay {existing} registros (máximo {max_total})."))
            return

        clientes = list(Cliente.objects.all())
        estados_orden = list(EstadoOrden.objects.all())
        estados_cafe = list(EstadoCafe.objects.all())

        if not clientes:
            self.stdout.write(self.style.WARNING("No hay clientes para asignar a las órdenes. Crea clientes primero."))
            return
        if not estados_orden:
            self.stdout.write(self.style.WARNING("No hay estados de orden. Crea estados de orden primero."))
            return
        if not estados_cafe:
            self.stdout.write(self.style.WARNING("No hay estados de café. Crea estados de café primero."))
            return

        now = timezone.now()

        new_orders = []
        for _ in range(to_create):
            cliente = random.choice(clientes)
            estado_orden = random.choice(estados_orden)
            estado_cafe = random.choice(estados_cafe)

            # Distribuir fechas: ingreso hace 0-20 días, orden hace 0-10 días, entrega en 0-20 días.
            delta_ingreso = timedelta(days=random.randint(0, 20))
            fecha_ingreso = now - delta_ingreso
            delta_orden = timedelta(days=random.randint(0, 10))
            fecha_orden = now - delta_orden
            delta_entrega = timedelta(days=random.randint(0, 20))
            fecha_entrega = now + delta_entrega

            # Flags aleatorios
            trilla = random.choice([True, False])
            selec_cafe_verde = random.choice([True, False])
            tueste_flag = random.choice([True, False])
            selec_cafe_tostado = random.choice([True, False])
            molienda_flag = random.choice([True, False])
            empaque_flag = random.choice([True, False])
            conf_trilla = trilla and random.choice([True, False])
            conf_sel_verde = selec_cafe_verde and random.choice([True, False])
            conf_tueste = tueste_flag and random.choice([True, False])
            conf_sel_tostado = selec_cafe_tostado and random.choice([True, False])
            conf_molienda = molienda_flag and random.choice([True, False])
            conf_empaque = empaque_flag and random.choice([True, False])

            prioridad = random.randint(1, 5)

            notas = random.choice([
                "Pedido regular",
                "Entrega urgente",
                "Verificar molienda",
                "Ajustar tueste",
                None,
            ])

            created_at = now - timedelta(days=random.randint(0, 30))
            updated_at = created_at + timedelta(days=random.randint(0, 10))

            new_orders.append(
                Orden(
                    cliente=cliente,
                    estado_orden=estado_orden,
                    estado_inven_cafe=estado_cafe,
                    fecha_ingreso=fecha_ingreso,
                    fecha_orden=fecha_orden,
                    fecha_entrega=fecha_entrega,
                    notas=notas,
                    trilla=trilla,
                    selec_cafe_verde=selec_cafe_verde,
                    tueste_flag=tueste_flag,
                    selec_cafe_tostado=selec_cafe_tostado,
                    molienda_flag=molienda_flag,
                    empaque_flag=empaque_flag,
                    conf_trilla=conf_trilla,
                    conf_sel_verde=conf_sel_verde,
                    conf_tueste=conf_tueste,
                    conf_sel_tostado=conf_sel_tostado,
                    conf_molienda=conf_molienda,
                    conf_empaque=conf_empaque,
                    prioridad=prioridad,
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )

        Orden.objects.bulk_create(new_orders, batch_size=100)

        self.stdout.write(self.style.SUCCESS(f"Se crearon {len(new_orders)} órdenes nuevas. Total ahora: {existing + len(new_orders)}."))
