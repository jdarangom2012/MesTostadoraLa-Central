from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import random
import string

from ordenes.models import Orden
from clientes.models import Cliente
from estado_ordenes.models import EstadoOrden
from empleados.models import Empleado


def rand_code(prefix: str, n: int = 2) -> str:
    # Genera un código corto para no exceder max_length=8 del campo 'orden'.
    return (prefix + ''.join(random.choice(string.digits) for _ in range(n)))[:8]


class Command(BaseCommand):
    help = "Smoke test: crea 3 órdenes, las edita y elimina para validar el flujo CRUD sin errores."

    def add_arguments(self, parser):
        parser.add_argument('--prefix', default='ORDSMK', help='Prefijo para códigos de orden generados')

    def _ensure_referentials(self):
        cliente, _ = Cliente.objects.get_or_create(nombre='Cliente Smoke', defaults={
            'apellidos': 'Test',
            'created_at': timezone.now(),
        })
        estado, _ = EstadoOrden.objects.get_or_create(estado_orden='En Espera')
        empleado = Empleado.objects.first()
        if not empleado:
            empleado = Empleado.objects.create(
                identificacion=rand_code('ID'),
                nombres='Empleado',
                apellidos='Smoke',
                estado='Activo',
                fecha_ingreso=timezone.now(),
            )
        return cliente, estado, empleado

    def handle(self, *args, **options):
        prefix = options['prefix']
        cliente, estado, empleado = self._ensure_referentials()

        created_ids = []
        self.stdout.write(self.style.NOTICE('Creando 3 órdenes...'))
        try:
            with transaction.atomic():
                for i in range(3):
                    codigo = rand_code(prefix, 2)
                    o = Orden.objects.create(
                        cliente=cliente,
                        estado_orden=estado,
                        id_empleado=empleado,
                        orden=codigo,
                        fecha_ingreso=timezone.now(),
                        fecha_inicio_orden=timezone.now(),
                        prioridad=1,
                    )
                    created_ids.append(o.id)
                    self.stdout.write(f" - Creada orden #{o.id} código {codigo}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fallo al crear órdenes: {e}"))
            return

        self.stdout.write(self.style.NOTICE('Editando órdenes...'))
        try:
            with transaction.atomic():
                for oid in created_ids:
                    o = Orden.objects.get(id=oid)
                    nuevo_codigo = f"{o.orden}E"
                    o.orden = nuevo_codigo
                    o.prioridad = 2
                    o.updated_at = timezone.now()
                    o.save()
                    self.stdout.write(f" - Editada orden #{o.id} nuevo código {nuevo_codigo}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fallo al editar órdenes: {e}"))
            return

        self.stdout.write(self.style.NOTICE('Eliminando órdenes...'))
        try:
            with transaction.atomic():
                for oid in created_ids:
                    Orden.objects.filter(id=oid).delete()
                    self.stdout.write(f" - Eliminada orden #{oid}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fallo al eliminar órdenes: {e}"))
            return

        remaining = Orden.objects.filter(id__in=created_ids).count()
        if remaining == 0:
            self.stdout.write(self.style.SUCCESS('Smoke test OK: CRUD de órdenes completado sin errores.'))
        else:
            self.stderr.write(self.style.ERROR('Smoke test incompleto: quedan órdenes sin eliminar.'))
