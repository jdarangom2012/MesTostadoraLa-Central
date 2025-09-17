from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms

from .models import TamanoEmpaque


class TamanoEmpaqueForm(forms.ModelForm):
    class Meta:
        model = TamanoEmpaque
        fields = ['tamano_empaque']
        widgets = {
            'tamano_empaque': forms.TextInput(attrs={'class': 'w-full input'}),
        }


@permission_required('tamano_empaque.view_tamanoempaque', raise_exception=True)
def listar_tamano_empaque(request):
    qs = TamanoEmpaque.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(tamano_empaque__icontains=search))
    qs = qs.order_by('tamano_empaque', 'id')

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
        return render(request, 'tamano_empaque/_modal_listar_TamanosEmpaque.html', ctx)
    return render(request, 'tamano_empaque/listar_TamanosEmpaque.html', ctx)


@require_http_methods(["GET", "POST"])
@permission_required('tamano_empaque.add_tamanoempaque', raise_exception=True)
def add_tamano_empaque(request):
    if request.method == 'POST':
        form = TamanoEmpaqueForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_tamano_empaque(request)
                return redirect('tamano_empaque_listar')
    else:
        form = TamanoEmpaqueForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'tamano_empaque/add_TamanoEmpaque.html', {'form': form})
    return render(request, 'tamano_empaque/listar_TamanosEmpaque.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('tamano_empaque.change_tamanoempaque', raise_exception=True)
def edit_tamano_empaque(request, pk):
    obj = get_object_or_404(TamanoEmpaque, pk=pk)
    if request.method == 'POST':
        form = TamanoEmpaqueForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_tamano_empaque(request)
                return redirect('tamano_empaque_listar')
    else:
        form = TamanoEmpaqueForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tamano_empaque/detail_TamanoEmpaque.html', {'form': form, 'obj': obj})
    return render(request, 'tamano_empaque/listar_TamanosEmpaque.html', {})


@permission_required('tamano_empaque.delete_tamanoempaque', raise_exception=True)
def delete_tamano_empaque(request, pk):
    obj = get_object_or_404(TamanoEmpaque, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_tamano_empaque(request)
        return redirect('tamano_empaque_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'tamano_empaque/confirm_delete_TamanoEmpaque.html', {'obj': obj})
    return render(request, 'tamano_empaque/listar_TamanosEmpaque.html', {})
