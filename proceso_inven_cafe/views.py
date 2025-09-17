from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms

from .models import ProcesoInvenCafe


class ProcesoInvenCafeForm(forms.ModelForm):
    class Meta:
        model = ProcesoInvenCafe
        fields = ['proceso_inven_cafe']
        widgets = {
            'proceso_inven_cafe': forms.TextInput(attrs={'class': 'w-full input'}),
        }


@permission_required('proceso_inven_cafe.view_procesoinvencafe', raise_exception=True)
def listar_proceso_inven_cafe(request):
    qs = ProcesoInvenCafe.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(proceso_inven_cafe__icontains=search))
    qs = qs.order_by('proceso_inven_cafe', 'id')

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
        return render(request, 'proceso_inven_cafe/_modal_listar_ProcesoInventarioCafe.html', ctx)
    return render(request, 'proceso_inven_cafe/listar_ProcesoInventarioCafe.html', ctx)


@require_http_methods(["GET", "POST"])
@permission_required('proceso_inven_cafe.add_procesoinvencafe', raise_exception=True)
def add_proceso_inven_cafe(request):
    if request.method == 'POST':
        form = ProcesoInvenCafeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_proceso_inven_cafe(request)
                return redirect('proceso_inven_cafe_listar')
    else:
        form = ProcesoInvenCafeForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'proceso_inven_cafe/add_ProcesoInventarioCafe.html', {'form': form})
    return render(request, 'proceso_inven_cafe/listar_ProcesoInventarioCafe.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('proceso_inven_cafe.change_procesoinvencafe', raise_exception=True)
def edit_proceso_inven_cafe(request, pk):
    obj = get_object_or_404(ProcesoInvenCafe, pk=pk)
    if request.method == 'POST':
        form = ProcesoInvenCafeForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_proceso_inven_cafe(request)
                return redirect('proceso_inven_cafe_listar')
    else:
        form = ProcesoInvenCafeForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'proceso_inven_cafe/detail_ProcesoInventarioCafe.html', {'form': form, 'obj': obj})
    return render(request, 'proceso_inven_cafe/listar_ProcesoInventarioCafe.html', {})


@permission_required('proceso_inven_cafe.delete_procesoinvencafe', raise_exception=True)
def delete_proceso_inven_cafe(request, pk):
    obj = get_object_or_404(ProcesoInvenCafe, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_proceso_inven_cafe(request)
        return redirect('proceso_inven_cafe_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'proceso_inven_cafe/confirm_delete_ProcesoInventarioCafe.html', {'obj': obj})
    return render(request, 'proceso_inven_cafe/listar_ProcesoInventarioCafe.html', {})
