from django.core.management.base import BaseCommand
from django.core.management import call_command
from clientes.models import Cliente

class Command(BaseCommand):
    help = "Ejecuta carga de catálogos base y luego genera clientes aleatorios (wrapper)."

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=50, help='Cantidad de clientes a generar (máx 50)')
        parser.add_argument('--force', action='store_true', help='Forzar generación adicional aunque ya existan')
        parser.add_argument('--skip-catalogos', action='store_true', help='No recrear / asegurar catálogos (solo clientes)')

    def handle(self, *args, **options):
        cantidad = min(options['cantidad'], 50)
        force = options['force']
        skip_catalogos = options['skip_catalogos']

        if not skip_catalogos:
            self.stdout.write(self.style.NOTICE('>>> Asegurando catálogos base (tipos / identificaciones / estados)...'))
            call_command('seed_catalogos_clientes')
        else:
            self.stdout.write(self.style.NOTICE('>>> Omitiendo preparación de catálogos por bandera --skip-catalogos'))

        before = Cliente.objects.count()
        self.stdout.write(self.style.NOTICE(f'>>> Clientes antes: {before}'))

        call_args = {'cantidad': cantidad}
        if force:
            call_args['force'] = True

        self.stdout.write(self.style.NOTICE(f'>>> Generando clientes (target {cantidad}{" force" if force else ""})...'))
        call_command('seed_clientes', **call_args)

        after = Cliente.objects.count()
        diff = after - before
        self.stdout.write(self.style.SUCCESS(f'>>> Total actual: {after} (nuevos: {diff if diff>0 else 0})'))
        if not force and diff < (cantidad - before) and before < cantidad:
            self.stdout.write(self.style.WARNING('Nota: algunos códigos ya existían y se saltaron; use --force para intentar completar.'))
        self.stdout.write(self.style.SUCCESS('Proceso completo.'))
