from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from ordenes.models import Orden

from .models import Empaque


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        oid = getattr(obj, 'id', None) or getattr(obj, 'pk', '')
        return f"Orden {oid}"


class EmpaqueForm(forms.ModelForm):
    orden = OrdenChoiceField(queryset=Orden.objects.none(), required=False, widget=forms.Select(attrs={'class': 'w-full select'}))
    class Meta:
        model = Empaque
        # No incluir fechas en el form (solo para ordenación, no visibles)
        fields = ['orden', 'molienda', 'estado_inven_cafe', 'estado_tareas', 'cant_empaque', 'cant_empacada', 'cant_etiquetas', 'emp_clientes', 'total_empaques', 'total_etiquetas', 'total_paquetes', 'notas']
        widgets = {
            'molienda': forms.Select(attrs={'class': 'w-full select'}),
            'estado_inven_cafe': forms.Select(attrs={'class': 'w-full select'}),
            'estado_tareas': forms.Select(attrs={'class': 'w-full select'}),
            'cant_empaque': forms.NumberInput(attrs={'class': 'w-full input'}),
            'cant_empacada': forms.NumberInput(attrs={'class': 'w-full input'}),
            'cant_etiquetas': forms.NumberInput(attrs={'class': 'w-full input'}),
            'emp_clientes': forms.NumberInput(attrs={'class': 'w-full input'}),
            'total_empaques': forms.NumberInput(attrs={'class': 'w-full input'}),
            'total_etiquetas': forms.NumberInput(attrs={'class': 'w-full input'}),
            'total_paquetes': forms.NumberInput(attrs={'class': 'w-full input'}),
            'notas': forms.TextInput(attrs={'class': 'w-full input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_qs = Orden.objects.all().order_by('-id')
        # Evitar errores en POST (orden fuera del top-N)
        if self.is_bound:
            self.fields['orden'].queryset = base_qs
        else:
            self.fields['orden'].queryset = base_qs.select_related('cliente')[:200]
        self.fields['orden'].empty_label = 'Seleccione una orden'


@permission_required('empaques.view_empaque', raise_exception=True)
def listar_empaque(request):
    qs = Empaque.objects.select_related('orden', 'molienda', 'estado_inven_cafe', 'estado_tareas')
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
@permission_required('empaques.add_empaque', raise_exception=True)
def add_empaque(request):
    if request.method == 'POST':
        form = EmpaqueForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                    return listar_empaque(request)
                return redirect('empaque_listar')
    else:
        form = EmpaqueForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'empaques/add_Empaque.html', {'form': form})
    return render(request, 'empaques/listar_Empaque.html', {})


@require_http_methods(["GET", "POST"])
@permission_required('empaques.change_empaque', raise_exception=True)
def edit_empaque(request, pk):
    obj = get_object_or_404(Empaque, pk=pk)
    if request.method == 'POST':
        form = EmpaqueForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
            else:
                if request.headers.get('X-Fragment'):
                    return listar_empaque(request)
                return redirect('empaque_listar')
    else:
        form = EmpaqueForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'empaques/detail_Empaque.html', {'form': form, 'obj': obj})
    return render(request, 'empaques/listar_Empaque.html', {})


@permission_required('empaques.delete_empaque', raise_exception=True)
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
