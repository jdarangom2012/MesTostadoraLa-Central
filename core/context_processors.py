def user_groups(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        groups = set(user.groups.values_list('name', flat=True))
    else:
        groups = set()
    groups_lower = {g.lower() for g in groups}
    can_view_clientes = bool(user and user.has_perm('clientes.view_cliente'))
    can_manage_clientes = bool(user and (user.has_perm('clientes.add_cliente') or user.has_perm('clientes.change_cliente') or user.has_perm('clientes.delete_cliente')))
    return {
        'USER_IS_STAFF': bool(user and user.is_staff),
        'USER_GROUPS': groups,
        'HAS_GROUP_CALIDAD': 'calidad' in groups_lower,
        'CAN_VIEW_CLIENTES': can_view_clientes,
        'CAN_MANAGE_CLIENTES': can_manage_clientes,
    }
