from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms

from .models import CafeEmpaque


class CafeEmpaqueForm(forms.ModelForm):
    class Meta:
        model = CafeEmpaque
        fields = ['empaque_cafe']
        widgets = {
            'empaque_cafe': forms.TextInput(attrs={'class': 'w-full input'}),
        }


@permission_required('cafe_empaque.view_cafeempaque', raise_exception=True)
def listar_cafe_empaque(request):
    qs = CafeEmpaque.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(empaque_cafe__icontains=search))
    qs = qs.order_by('empaque_cafe', 'id')

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
        return render(request, 'cafe_empaque/_modal_listar_EmpaqueCafe.html', ctx)
    return render(request, 'cafe_empaque/listar_EmpaqueCafe.html', ctx)


@require_http_methods(["GET", "POST"])
@permission_required('cafe_empaque.add_cafeempaque', raise_exception=True)
def add_cafe_empaque(request):
    if request.method == 'POST':
        form = CafeEmpaqueForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_cafe_empaque(request)
                return redirect('cafe_empaque_listar')
    else:
        form = CafeEmpaqueForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'cafe_empaque/add_EmpaqueCafe.html', {'form': form})
    return render(request, 'cafe_empaque/listar_EmpaqueCafe.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('cafe_empaque.change_cafeempaque', raise_exception=True)
def edit_cafe_empaque(request, pk):
    obj = get_object_or_404(CafeEmpaque, pk=pk)
    if request.method == 'POST':
        form = CafeEmpaqueForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_cafe_empaque(request)
                return redirect('cafe_empaque_listar')
    else:
        form = CafeEmpaqueForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'cafe_empaque/detail_EmpaqueCafe.html', {'form': form, 'obj': obj})
    return render(request, 'cafe_empaque/listar_EmpaqueCafe.html', {})


@permission_required('cafe_empaque.delete_cafeempaque', raise_exception=True)
def delete_cafe_empaque(request, pk):
    obj = get_object_or_404(CafeEmpaque, pk=pk)
    if request.method == 'POST':
        obj.delete()
        if request.headers.get('X-Fragment'):
            return listar_cafe_empaque(request)
        return redirect('cafe_empaque_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'cafe_empaque/confirm_delete_EmpaqueCafe.html', {'obj': obj})
    return render(request, 'cafe_empaque/listar_EmpaqueCafe.html', {})
