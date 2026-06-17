from django.shortcuts import render, get_object_or_404, redirect
from seguridad.decorators import permiso_accion_requerido
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from django.db.models import Q
import re

from .models import CurvaTueste


class CurvaTuesteForm(forms.ModelForm):
    class Meta:
        model = CurvaTueste
        # fecha_ingreso es automática (no se muestra ni se edita)
        fields = ['temp_set_point', 'temp_tost', 'porcentaje_aire', 'porcentaje_gas']
        widgets = {
            'temp_set_point': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1'}),
            'temp_tost': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1'}),
            'porcentaje_aire': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1', 'min': '0', 'max': '100'}),
            'porcentaje_gas': forms.NumberInput(attrs={'class': 'w-full input', 'step': '1', 'min': '0', 'max': '100'}),
        }


@permiso_accion_requerido('curvas_tueste.view_curvatueste', 'ver_curvas_tueste')
def listar_curvas_tueste(request):
    qs = CurvaTueste.objects.all().order_by('-fecha_ingreso', '-id')
    search = request.GET.get('q', '').strip()
    if search:
        # Buscar por Id y coincidencias exactas numéricas en otros campos
        filters = Q()
        # Buscar patrón "Curva 123" o cualquier número suelto
        m = re.search(r"(?:^|\b)curva\s*(\d+)\b", search, flags=re.IGNORECASE) or re.search(r"\b(\d+)\b", search)
        if m:
            try:
                n = int(m.group(1))
                filters |= Q(id=n) | Q(temp_set_point=n) | Q(temp_tost=n) | Q(porcentaje_aire=n) | Q(porcentaje_gas=n)
            except ValueError:
                pass
        qs = qs.filter(filters)

    paginator = Paginator(qs, 7)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    ctx = {
        'curvas': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'search': search,
    }
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'curvas_tueste/_modal_listar_CurvasTueste.html', ctx)
    return render(request, 'curvas_tueste/listar_CurvasTueste.html', ctx)


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('curvas_tueste.add_curvatueste', 'crear_curvas_tueste')
def add_curva_tueste(request):
    if request.method == 'POST':
        form = CurvaTuesteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # La fecha la maneja la BD por default; opcionalmente se podría setear aquí.
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_curvas_tueste(request)
            return redirect('curvas_tueste_listar')
    else:
        form = CurvaTuesteForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        # Nota: el usuario pidió nombre add_Empaque.html
        return render(request, 'curvas_tueste/add_Empaque.html', {'form': form})
    return render(request, 'curvas_tueste/listar_CurvasTueste.html', {})


@require_http_methods(["GET", "POST"])
@permiso_accion_requerido('curvas_tueste.change_curvatueste', 'editar_curvas_tueste')
def edit_curva_tueste(request, pk):
    obj = get_object_or_404(CurvaTueste, pk=pk)
    if request.method == 'POST':
        form = CurvaTuesteForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Fragment'):
                return listar_curvas_tueste(request)
            return redirect('curvas_tueste_listar')
    else:
        form = CurvaTuesteForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'curvas_tueste/detail_CurvasTueste.html', {'form': form, 'obj': obj})
    return render(request, 'curvas_tueste/listar_CurvasTueste.html', {})


@permiso_accion_requerido('curvas_tueste.delete_curvatueste', 'eliminar_curvas_tueste')
def delete_curva_tueste(request, pk):
    obj = get_object_or_404(CurvaTueste, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_curvas_tueste(request)
        return redirect('curvas_tueste_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'curvas_tueste/confirm_delete_CurvasTueste.html', {'obj': obj})
    return render(request, 'curvas_tueste/listar_CurvasTueste.html', {})
