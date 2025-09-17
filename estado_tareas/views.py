from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms

from .models import EstadoTarea


class EstadoTareaForm(forms.ModelForm):
    class Meta:
        model = EstadoTarea
        fields = ['estado_tareas']
        widgets = {
            'estado_tareas': forms.TextInput(attrs={'class': 'w-full input'}),
        }


@permission_required('estado_tareas.view_estadotarea', raise_exception=True)
def listar_estado_tareas(request):
    qs = EstadoTarea.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(estado_tareas__icontains=search))
    qs = qs.order_by('estado_tareas', 'id')

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
        return render(request, 'estado_tareas/_modal_listar_EstadoTareas.html', ctx)
    return render(request, 'estado_tareas/listar_EstadoTareas.html', ctx)


@require_http_methods(["GET", "POST"])
@permission_required('estado_tareas.add_estadotarea', raise_exception=True)
def add_estado_tareas(request):
    if request.method == 'POST':
        form = EstadoTareaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_estado_tareas(request)
                return redirect('estado_tareas_listar')
    else:
        form = EstadoTareaForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'estado_tareas/add_EstadoTareas.html', {'form': form})
    return render(request, 'estado_tareas/listar_EstadoTareas.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('estado_tareas.change_estadotarea', raise_exception=True)
def edit_estado_tareas(request, pk):
    obj = get_object_or_404(EstadoTarea, pk=pk)
    if request.method == 'POST':
        form = EstadoTareaForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_estado_tareas(request)
                return redirect('estado_tareas_listar')
    else:
        form = EstadoTareaForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'estado_tareas/detail_EstadoTareas.html', {'form': form, 'obj': obj})
    return render(request, 'estado_tareas/listar_EstadoTareas.html', {})


@permission_required('estado_tareas.delete_estadotarea', raise_exception=True)
def delete_estado_tareas(request, pk):
    obj = get_object_or_404(EstadoTarea, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_estado_tareas(request)
        return redirect('estado_tareas_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'estado_tareas/confirm_delete_EstadoTareas.html', {'obj': obj})
    return render(request, 'estado_tareas/listar_EstadoTareas.html', {})
