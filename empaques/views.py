from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db import transaction
from seguridad.decorators import permiso_accion_requerido
from seguridad.helpers import normalizar

from .forms import EmpaqueForm, build_detalle_empaque_formset
from .models import Empaque


EMPAQUE_CAMPOS_OPERATIVOS = {'cant_etiquetas', 'emp_clientes'}
EMPAQUE_ROLES_RESTRINGIDOS = {'tostador', 'empacador'}
EMPAQUE_ROLES_ACCESO_TOTAL = {'administrador', 'admin', 'coordinador'}
def obtener_roles_usuario(user):
    if not user or not getattr(user, 'is_authenticated', False):
        return set()

    roles = set()

    if getattr(user, 'is_superuser', False):
        roles.add('administrador')

    perfil = getattr(user, 'perfilusuario', None) or getattr(user, 'profile', None)
    rol = getattr(perfil, 'rol', None)
    nombre_rol = normalizar(getattr(rol, 'nombre', ''))
    if nombre_rol:
        roles.add(nombre_rol)

    try:
        roles.update(normalizar(nombre) for nombre in user.groups.values_list('name', flat=True))
    except Exception:
        pass

    return {rol for rol in roles if rol}


def usuario_con_restriccion_empaque(user) -> bool:
    roles = obtener_roles_usuario(user)
    if roles & EMPAQUE_ROLES_ACCESO_TOTAL:
        return False
    return bool(roles & EMPAQUE_ROLES_RESTRINGIDOS)


def aplicar_restricciones_form_empaque(form):
    if not usuario_con_restriccion_empaque(getattr(form, '_request_user', None)):
        return

    for field_name, field in form.fields.items():
        css = field.widget.attrs.get('class', '')
        if field_name in EMPAQUE_CAMPOS_OPERATIVOS:
            field.disabled = False
            field.widget.attrs.pop('disabled', None)
            field.widget.attrs.pop('readonly', None)
            field.widget.attrs['class'] = f"{css} ring-1 ring-brand-primary/30".strip()
            continue

        field.disabled = True
        field.widget.attrs['disabled'] = 'disabled'
        field.widget.attrs['aria-readonly'] = 'true'
        field.widget.attrs['class'] = f"{css} bg-gray-100 text-gray-500 cursor-not-allowed opacity-90".strip()


def proteger_campos_empaque_restringidos(obj, original, user):
    if not usuario_con_restriccion_empaque(user):
        return

    for campo in EmpaqueForm.Meta.fields:
        if campo in EMPAQUE_CAMPOS_OPERATIVOS:
            continue
        setattr(obj, campo, getattr(original, campo))


def valor_entero_seguro(valor):
    try:
        return int(valor or 0)
    except (TypeError, ValueError):
        return 0


def sincronizar_resumen_empaque(instance):
    detalles = list(
        instance.detalles.select_related('tamano_empaque', 'nivel_molienda').order_by('id')
    )

    if not detalles:
        return

    primer_detalle = detalles[0]
    total_pedido = sum(valor_entero_seguro(detalle.pedido) for detalle in detalles)
    total_empacado = sum(valor_entero_seguro(detalle.empacado) for detalle in detalles)

    instance.tamano = primer_detalle.tamano_empaque
    instance.nivel_molienda = primer_detalle.nivel_molienda
    instance.cant_empaque = total_pedido
    instance.cant_empacada = total_empacado
    instance.total_empaques = total_pedido
    instance.total_paquetes = total_empacado
    instance.save()


@permiso_accion_requerido(codigo='ver_empaque')
def listar_empaque(request):
    qs = Empaque.objects.select_related('orden', 'orden__cliente', 'nivel_molienda', 'estado_inven_cafe', 'estado_tareas')
    search = request.GET.get('q', '').strip()
    if search:
        num = None
        try:
            num = int(search)
        except (TypeError, ValueError):
            num = None
        q = Q(estado_tareas__estado_tareas__icontains=search) | Q(notas__icontains=search)
        if num is not None:
            q = q | Q(orden__id=num)
        qs = qs.filter(q)
    qs = qs.order_by('-id')

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    ctx = {
        'items': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'empaques/_modal_listar_Empaque.html', ctx)
    return render(request, 'empaques/listar_Empaque.html', ctx)


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('empaques.add_empaque', 'crear_empaque')
def add_empaque(request):
    if request.method == 'POST':
        form = EmpaqueForm(request.POST)
        detalle_formset = build_detalle_empaque_formset(data=request.POST, instance=form.instance)
        detalle_formset_valid = detalle_formset.is_valid()
        if form.is_valid() and detalle_formset_valid:
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    detalle_formset.instance = obj
                    detalle_formset.save()
                    sincronizar_resumen_empaque(obj)
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_empaque(request)
                return redirect('empaque_listar')
    else:
        form = EmpaqueForm()
        detalle_formset = build_detalle_empaque_formset(instance=form.instance)
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'empaques/add_Empaque.html', {'form': form, 'detalle_formset': detalle_formset})
    return render(request, 'empaques/listar_Empaque.html', {})


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('empaques.change_empaque', 'editar_empaque')
def edit_empaque(request, pk):
    obj = get_object_or_404(Empaque, pk=pk)
    user_has_empaque_restrictions = usuario_con_restriccion_empaque(request.user)
    if request.method == 'POST':
        form = EmpaqueForm(request.POST, instance=obj)
        form._request_user = request.user
        detalle_formset = build_detalle_empaque_formset(data=request.POST, instance=obj)
        if user_has_empaque_restrictions:
            aplicar_restricciones_form_empaque(form)
        detalle_formset_valid = detalle_formset.is_valid()
        if form.is_valid() and detalle_formset_valid:
            try:
                with transaction.atomic():
                    inst = form.save(commit=False)
                    proteger_campos_empaque_restringidos(inst, obj, request.user)
                    inst.save()
                    detalle_formset.instance = inst
                    detalle_formset.save()
                    sincronizar_resumen_empaque(inst)
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_empaque(request)
                return redirect('empaque_listar')
    else:
        form = EmpaqueForm(instance=obj)
        form._request_user = request.user
        detalle_formset = build_detalle_empaque_formset(instance=obj)
        if user_has_empaque_restrictions:
            aplicar_restricciones_form_empaque(form)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(
            request,
            'empaques/detail_Empaque.html',
            {
                'form': form,
                'obj': obj,
                'detalle_formset': detalle_formset,
                'user_has_empaque_restrictions': user_has_empaque_restrictions,
                'empaque_campos_operativos': sorted(EMPAQUE_CAMPOS_OPERATIVOS),
            },
        )
    return render(request, 'empaques/listar_Empaque.html', {})


@permiso_accion_requerido('empaques.delete_empaque', 'eliminar_empaque')
def delete_empaque(request, pk):
    obj = get_object_or_404(Empaque, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_empaque(request)
        return redirect('empaque_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'empaques/confirm_delete_Empaque.html', {'obj': obj})
    return render(request, 'empaques/listar_Empaque.html', {})
