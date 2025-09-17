from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

# Definición por rol: permisos explícitos y apps con acciones a aplicar a todos sus modelos
ROLE_DEFS = {
    'consulta': {
        'perms': [
            'clientes.view_cliente',
        ],
        'apps': {
            # Solo lectura en módulos operativos
            'ordenes': ['view'],
            'ordenes_trilla': ['view'],
            'tueste': ['view'],
            'molienda': ['view'],
            'inventario_cafe': ['view'],
            'materiales': ['view'],
            'proceso_inven_cafe': ['view'],
            'cafe_empaque': ['view'],
            'empaques': ['view'],
            'curvas_tueste': ['view'],
            'variedad_cafe': ['view'],
            'zaranda_grupo': ['view'],
            'estado_cafe': ['view'],
            'estado_inven_cafe': ['view'],
            'estado_ordenes': ['view'],
            'estado_tareas': ['view'],
            'nivel_molienda': ['view'],
            'nivel_tueste': ['view'],
            'origen_cafe': ['view'],
            'tamano_empaque': ['view'],
            'tipo_clientes': ['view'],
            'tipo_identificacion': ['view'],
            'estados_clientes': ['view'],
            # apps con vistas sin modelos (posible 0 permisos):
            'reportes': ['view'],
            'variendad_inven_cafe': ['view'],
        }
    },
    'operador': {
        'perms': [
            'clientes.view_cliente', 'clientes.add_cliente', 'clientes.change_cliente',
        ],
        'apps': {
            # Operación: ver + crear/editar
            'ordenes': ['view','add','change'],
            'ordenes_trilla': ['view','add','change'],
            'tueste': ['view','add','change'],
            'molienda': ['view','add','change'],
            'inventario_cafe': ['view','add','change'],
            'materiales': ['view','add','change'],
            'proceso_inven_cafe': ['view','add','change'],
            'cafe_empaque': ['view','add','change'],
            'empaques': ['view','add','change'],
            'curvas_tueste': ['view','add','change'],
            'variedad_cafe': ['view','add','change'],
            'zaranda_grupo': ['view','add','change'],
            'estado_cafe': ['view','add','change'],
            'estado_inven_cafe': ['view','add','change'],
            'estado_ordenes': ['view','add','change'],
            'estado_tareas': ['view','add','change'],
            'nivel_molienda': ['view','add','change'],
            'nivel_tueste': ['view','add','change'],
            'origen_cafe': ['view','add','change'],
            'tamano_empaque': ['view','add','change'],
            'tipo_clientes': ['view','add','change'],
            'tipo_identificacion': ['view','add','change'],
            'estados_clientes': ['view','add','change'],
            'variendad_inven_cafe': ['view','add','change'],
        }
    },
    'supervisor': {
        'perms': [
            'clientes.view_cliente', 'clientes.add_cliente', 'clientes.change_cliente', 'clientes.delete_cliente',
        ],
        'apps': {
            # Supervisor: ver + crear/editar/eliminar
            'ordenes': ['view','add','change','delete'],
            'ordenes_trilla': ['view','add','change','delete'],
            'tueste': ['view','add','change','delete'],
            'molienda': ['view','add','change','delete'],
            'inventario_cafe': ['view','add','change','delete'],
            'materiales': ['view','add','change','delete'],
            'proceso_inven_cafe': ['view','add','change','delete'],
            'cafe_empaque': ['view','add','change','delete'],
            'empaques': ['view','add','change','delete'],
            'curvas_tueste': ['view','add','change','delete'],
            'variedad_cafe': ['view','add','change','delete'],
            'zaranda_grupo': ['view','add','change','delete'],
            'estado_cafe': ['view','add','change','delete'],
            'estado_inven_cafe': ['view','add','change','delete'],
            'estado_ordenes': ['view','add','change','delete'],
            'estado_tareas': ['view','add','change','delete'],
            'nivel_molienda': ['view','add','change','delete'],
            'nivel_tueste': ['view','add','change','delete'],
            'origen_cafe': ['view','add','change','delete'],
            'tamano_empaque': ['view','add','change','delete'],
            'tipo_clientes': ['view','add','change','delete'],
            'tipo_identificacion': ['view','add','change','delete'],
            'estados_clientes': ['view','add','change','delete'],
            'variendad_inven_cafe': ['view','add','change','delete'],
        }
    },
}

class Command(BaseCommand):
    help = 'Crea grupos (roles) básicos y asigna permisos predefinidos por app y acción.'

    def add_app_perms(self, group: Group, app_label: str, actions: list[str]) -> int:
        added = 0
        for action in actions:
            # Agrega todos los permisos del tipo <action>_* para el app_label indicado
            qs = Permission.objects.filter(content_type__app_label=app_label, codename__startswith=f"{action}_")
            count = qs.count()
            if count == 0:
                self.stderr.write(self.style.WARNING(f"Sin permisos para {app_label}.{action}_* (¿app sin modelos o sin migraciones?)"))
                continue
            group.permissions.add(*qs)
            added += count
        return added

    def handle(self, *args, **options):
        total_added = 0
        for role, cfg in ROLE_DEFS.items():
            group, _ = Group.objects.get_or_create(name=role)
            added = 0
            # Permisos explícitos app.codename
            for label in cfg.get('perms', []):
                try:
                    app_label, codename = label.split('.')
                except ValueError:
                    self.stderr.write(self.style.WARNING(f"Permiso mal formateado: {label}"))
                    continue
                try:
                    perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                except Permission.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f"No existe permiso: {label}"))
                    continue
                group.permissions.add(perm)
                added += 1
            # Permisos por apps (acciones aplicadas a todos los modelos del app)
            for app_label, actions in (cfg.get('apps') or {}).items():
                added += self.add_app_perms(group, app_label, actions)
            total_added += added
            self.stdout.write(self.style.SUCCESS(f"Rol '{role}' listo. Permisos añadidos/asegurados: {added}"))

        self.stdout.write(self.style.SUCCESS(f'Roles y permisos configurados. Total asignados: {total_added}'))
