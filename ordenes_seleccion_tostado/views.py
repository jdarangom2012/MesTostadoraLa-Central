from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from django.utils import timezone

from .models import OrdenSeleccionTostado
from ordenes.models import Orden
from estado_ordenes.models import EstadoOrden
from inventario_cafe.models import InventarioCafe


class OrdenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Orden {obj.id}"


class InventarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Mostrar solo el código del inventario
        return obj.codigo or f"INV-{obj.id:06d}"


class OrdenSeleccionTostadoForm(forms.ModelForm):
    orden = OrdenChoiceField(
        queryset=Orden.objects.all().order_by('-id'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    inventario_cafe_ref = InventarioChoiceField(
        queryset=InventarioCafe.objects.all().order_by('-id'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )
    estado_tareas = forms.ModelChoiceField(
        queryset=EstadoOrden.objects.all().order_by('estado_orden'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full select'})
    )

    class Meta:
        model = OrdenSeleccionTostado
        fields = [
            'orden',
            'inventario_cafe_ref',
            'estado_tareas',
            'cat_limpieza',
            'cat_quaker','peso_quaker',
            'cat_grupo1','desc_grupo1','peso_grupo1',
            'cat_grupo2','desc_grupo2','peso_grupo2',
            'cat_grupo3','desc_grupo3','peso_grupo3',
        ]
        widgets = {
            'cat_limpieza': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'cat_quaker': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'peso_quaker': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo1': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo1': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo1': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo2': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo2': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo2': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
            'cat_grupo3': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'desc_grupo3': forms.TextInput(attrs={'class': 'w-full input'}),
            'peso_grupo3': forms.NumberInput(attrs={'class': 'w-full input', 'step': '0.01'}),
        }


@permission_required('ordenes_seleccion_tostado.view_ordenselecciontostado', raise_exception=True)
def listar_ordenes_seleccion_tostado(request):
    qs = (
        OrdenSeleccionTostado.objects
        .select_related('estado_tareas', 'orden', 'orden__cliente', 'cafe', 'inventario_cafe_ref')
        .order_by('-fecha_ingreso','-id')
    )
    search = request.GET.get('q', '').strip()
    if search:
        if search.isdigit():
            qs = qs.filter(id=int(search))
        else:
            qs = qs.filter(
                Q(estado_tareas__estado_orden__icontains=search) |
                Q(desc_grupo1__icontains=search) |
                Q(desc_grupo2__icontains=search) |
                Q(desc_grupo3__icontains=search)
            )

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
        return render(request, 'ordenes_seleccion_tostado/_modal_listar_OrdenesSelecionTostado.html', ctx)
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', ctx)


@require_http_methods(["GET","POST"])
@permission_required('ordenes_seleccion_tostado.add_ordenselecciontostado', raise_exception=True)
def add_orden_seleccion_tostado(request):
    if request.method == 'POST':
        form = OrdenSeleccionTostadoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.fecha_ingreso:
                obj.fecha_ingreso = timezone.now()
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            obj.save()
            if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
                return listar_ordenes_seleccion_tostado(request)
            return redirect('ordenes_seleccion_tostado_listar')
    else:
        form = OrdenSeleccionTostadoForm()
    if request.headers.get('X-Fragment') or request.GET.get('fragment') == '1':
        return render(request, 'ordenes_seleccion_tostado/add_OrdenesSelecionTostado.html', {'form': form})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})


@require_http_methods(["GET","POST"])
@permission_required('ordenes_seleccion_tostado.change_ordenselecciontostado', raise_exception=True)
def edit_orden_seleccion_tostado(request, pk):
    obj = get_object_or_404(OrdenSeleccionTostado, pk=pk)
    if request.method == 'POST':
        form = OrdenSeleccionTostadoForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.updated_at = timezone.now()
            inst.save()
            if request.headers.get('X-Fragment'):
                return listar_ordenes_seleccion_tostado(request)
            return redirect('ordenes_seleccion_tostado_listar')
    else:
        form = OrdenSeleccionTostadoForm(instance=obj)
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_tostado/detail_OrdenesSelecionTostado.html', {'form': form, 'obj': obj})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})


@permission_required('ordenes_seleccion_tostado.delete_ordenselecciontostado', raise_exception=True)
def delete_orden_seleccion_tostado(request, pk):
    obj = get_object_or_404(OrdenSeleccionTostado, pk=pk)
    if request.method == 'POST':
        obj.delete()
        is_fragment = bool(request.headers.get('X-Fragment')) or request.POST.get('fragment') == '1'
        if is_fragment:
            return listar_ordenes_seleccion_tostado(request)
        return redirect('ordenes_seleccion_tostado_listar')
    if request.GET.get('fragment') == '1' or request.headers.get('X-Fragment'):
        return render(request, 'ordenes_seleccion_tostado/confirm_delete_OrdenesSelecionTostado.html', {'t': obj})
    return render(request, 'ordenes_seleccion_tostado/listar_OrdenesSelecionTostado.html', {})
