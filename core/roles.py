from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Basic permission mapping per role. Adjust as needed.
ROLE_PERMISSIONS = {
    'operador': [
        # Read-only across core domain models
        ('view', 'orden'),
        ('view', 'material'),
        ('view', 'inventariocafe'),
        ('view', 'tueste'),
        ('view', 'molienda'),
    ],
    'coordinador': [
        # Read + add/update limited
        ('view', 'orden'), ('add', 'orden'), ('change', 'orden'),
        ('view', 'material'), ('add', 'material'), ('change', 'material'),
        ('view', 'tueste'), ('add', 'tueste'), ('change', 'tueste'),
        ('view', 'molienda'), ('add', 'molienda'), ('change', 'molienda'),
    ],
    # 'admin' will be superuser via signup, no explicit mapping needed
}


def assign_role_permissions():
    """Assign mapped permissions to roles if the Permission objects exist.
    Missing content types are ignored gracefully (e.g., if model not migrated yet).
    """
    for role, perms in ROLE_PERMISSIONS.items():
        try:
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            continue
        perm_objs = []
        for action, model in perms:
            try:
                # Find permission codename pattern: <action>_<model>
                codename = f"{action}_{model}"
                perm = Permission.objects.get(codename=codename)
                perm_objs.append(perm)
            except Permission.DoesNotExist:
                continue
        if perm_objs:
            group.permissions.add(*perm_objs)
