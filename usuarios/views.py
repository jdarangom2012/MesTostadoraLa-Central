from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q

@login_required
@user_passes_test(lambda u: u.is_staff)
def listar_usuarios(request):
    q = request.GET.get('q','').strip()
    users = User.objects.all().select_related('profile' if hasattr(User, 'profile') else None)
    if q:
        users = users.filter(
            Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    users = users.order_by('username')
    groups = Group.objects.all().order_by('name')
    perms = Permission.objects.select_related('content_type').order_by('content_type__app_label','codename')
    ctx = {
        'users': users,
        'groups': groups,
        'perms': perms,
        'search': q,
    }
    return render(request, 'usuarios/listar_usuarios.html', ctx)
