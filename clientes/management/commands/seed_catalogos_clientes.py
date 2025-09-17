from django.core.management.base import BaseCommand
from tipo_clientes.models import TipoCliente
from tipo_identificacion.models import TipoIdentificacion
from estados_clientes.models import EstadoCliente

TIPOS_CLIENTE = [
    "Minorista","Mayorista","Distribuidor","Exportador","Online","Corporativo"
]
TIPOS_IDENTIFICACION = [
    "DNI","RUC","Pasaporte","Carnet Extranjería","Licencia","Otro"
]
ESTADOS_CLIENTE = [
    "Activo","Inactivo","Suspendido","Bloqueado","Prospecto","VIP"
]

class Command(BaseCommand):
    help = "Crea datos base para catálogos de clientes (tipo cliente, tipo identificación, estado)."

    def handle(self, *args, **options):
        created = 0
        for nombre in TIPOS_CLIENTE:
            obj, was = TipoCliente.objects.get_or_create(tipo_cliente=nombre, defaults={'estado': True})
            if was: created += 1
        for nombre in TIPOS_IDENTIFICACION:
            obj, was = TipoIdentificacion.objects.get_or_create(tipo_identificacion=nombre, defaults={'estado': True})
            if was: created += 1
        for nombre in ESTADOS_CLIENTE:
            obj, was = EstadoCliente.objects.get_or_create(estado_cliente=nombre)
            if was: created += 1
        self.stdout.write(self.style.SUCCESS(f"Catálogos preparados. Nuevos registros: {created}"))
