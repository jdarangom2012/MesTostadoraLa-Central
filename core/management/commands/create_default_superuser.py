import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea un superusuario usando variables de entorno si no existe"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'Admin123!')
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Ya existe el usuario '{username}'"))
            return
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superusuario creado: {username}/{password}"))