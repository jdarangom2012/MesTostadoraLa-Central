import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from clientes.models import Cliente
from tipo_clientes.models import TipoCliente
from tipo_identificacion.models import TipoIdentificacion
from estados_clientes.models import EstadoCliente

NOMBRES = [
    "Carlos","María","Lucía","Pedro","Ana","Juan","Sofía","Luis","Miguel","Elena",
    "Jorge","Valentina","Andrés","Paula","Ricardo","Camila","Gustavo","Daniela","Rosa","Héctor",
]
APELLIDOS = [
    "García","Rodríguez","López","Martínez","Pérez","Gómez","Sánchez","Díaz","Ramírez","Torres",
    "Flores","Vargas","Castro","Suárez","Mendoza","Herrera","Chávez","Morales","Guzmán","Rojas",
]
CALLES = [
    "Av. Central","Calle Norte","Pasaje Sur","Av. Libertad","Calle Real","Av. Los Olivos","Calle 5","Av. Sol","Calle 12","Av. Progreso",
]
DOMINIOS = ["empresa.com","correo.com","mail.com","negocio.com","example.org"]

class Command(BaseCommand):
    help = "Genera hasta 50 clientes aleatorios"

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=50, help='Cantidad de clientes (máx 50)')
        parser.add_argument('--force', action='store_true', help='Ignorar tope si ya existen (solo para pruebas)')

    def handle(self, *args, **options):
        cantidad = min(options['cantidad'], 50)
        existentes = Cliente.objects.count()
        if existentes >= cantidad and not options['force']:
            self.stdout.write(self.style.WARNING(f"Ya existen {existentes} clientes. Use --force para forzar creación adicional."))
            return

        # Catálogos requeridos
        tipo_clientes = list(TipoCliente.objects.all()[:5])
        tipos_id = list(TipoIdentificacion.objects.all()[:5])
        estados = list(EstadoCliente.objects.all()[:5])
        if not (tipo_clientes and tipos_id and estados):
            self.stdout.write(self.style.ERROR("Se requieren registros en TipoCliente, TipoIdentificacion y EstadoCliente para asignar llaves foráneas."))
            return

        creados = 0
        objetivo = cantidad - existentes if existentes < cantidad else (cantidad if options['force'] else 0)
        for i in range(objetivo):
            nombre = random.choice(NOMBRES)
            apellido = random.choice(APELLIDOS)
            codigo = f"CL{random.randint(1000,9999)}"
            if Cliente.objects.filter(codigo=codigo).exists():
                continue
            email = f"{nombre.lower()}.{apellido.lower()}@{random.choice(DOMINIOS)}"
            direccion = f"{random.choice(CALLES)} #{random.randint(10,999)}"
            telefono = f"9{random.randint(10000000, 99999999)}"
            fecha_ingreso = timezone.now() - timedelta(days=random.randint(0,365))
            cliente = Cliente(
                codigo=codigo,
                nombre=nombre,
                apellidos=apellido,
                telefono=telefono,
                direccion=direccion,
                email=email[:30],
                fecha_ingreso=fecha_ingreso,
                created_at=fecha_ingreso,
                id_tipo_cliente=random.choice(tipo_clientes),
                id_tipo_identificacion=random.choice(tipos_id),
                id_estado_cliente=random.choice(estados)
            )
            cliente.save()
            creados += 1
        self.stdout.write(self.style.SUCCESS(f"Clientes creados: {creados}"))
