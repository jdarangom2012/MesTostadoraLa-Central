from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from .helpers import tiene_permiso_accion


def es_peticion_fragmento(request) -> bool:
    return bool(
        request.headers.get('HX-Request')
        or request.headers.get('X-Fragment')
        or request.GET.get('fragment') == '1'
    )


def responder_permiso_denegado(request, message: str, status_code: int = 403):
    if es_peticion_fragmento(request):
        return render(
            request,
            'includes/_modal_permiso_denegado.html',
            {'message': message},
            status=status_code,
        )

    raise PermissionDenied


def permiso_accion_requerido(django_perm: str | None = None, codigo: str | None = None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if tiene_permiso_accion(request.user, django_perm=django_perm, codigo=codigo):
                return view_func(request, *args, **kwargs)

            return responder_permiso_denegado(request, 'No tienes permiso para realizar esta acción.')

        return _wrapped

    return decorator