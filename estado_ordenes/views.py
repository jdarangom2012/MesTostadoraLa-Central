from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms

from .models import EstadoOrden


class EstadoOrdenForm(forms.ModelForm):
    class Meta:
        model = EstadoOrden
        fields = ['estado_orden']
        widgets = {
            'estado_orden': forms.TextInput(attrs={'class': 'w-full input'}),
        }


@permission_required('estado_ordenes.view_estadoorden', raise_exception=True)
def listar_estado_orden(request):
    qs = EstadoOrden.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(estado_orden__icontains=search))
    qs = qs.order_by('estado_orden','id')

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
        return render(request, 'estado_ordenes/_modal_listar_EstadoOrden.html', ctx)
    return render(request, 'estado_ordenes/listar_EstadoOrden.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('estado_ordenes.add_estadoorden', raise_exception=True)
def add_estado_orden(request):
    if request.method == 'POST':
        form = EstadoOrdenForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_estado_orden(request)
                return redirect('estado_orden_listar')
    else:
        form = EstadoOrdenForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'estado_ordenes/add_EstadoOrden.html', {'form': form})
    return render(request, 'estado_ordenes/listar_EstadoOrden.html', {})


@require_http_methods(["GET","POST"])
@permission_required('estado_ordenes.change_estadoorden', raise_exception=True)
def edit_estado_orden(request, pk):
    obj = get_object_or_404(EstadoOrden, pk=pk)
    if request.method == 'POST':
        form = EstadoOrdenForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_estado_orden(request)
                return redirect('estado_orden_listar')
    else:
        form = EstadoOrdenForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'estado_ordenes/detail_EstadoOrden.html', {'form': form, 'obj': obj})
    return render(request, 'estado_ordenes/listar_EstadoOrden.html', {})


@permission_required('estado_ordenes.delete_estadoorden', raise_exception=True)
def delete_estado_orden(request, pk):
    obj = get_object_or_404(EstadoOrden, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_estado_orden(request)
        return redirect('estado_orden_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'estado_ordenes/confirm_delete_EstadoOrden.html', {'obj': obj})
    return render(request, 'estado_ordenes/listar_EstadoOrden.html', {})
